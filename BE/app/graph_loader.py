# Tải mạng đường bằng OSMnx (cả TP.HCM hoặc một quận); lưu vào MySQL nếu có, cache .graphml trong thư mục data/
import logging
import time

import networkx as nx
import osmnx as ox
import requests
from osmnx._errors import ResponseStatusCodeError
from sqlalchemy.orm import sessionmaker

from app import repository
from app.config import settings

logger = logging.getLogger(__name__)

# Mặc định OSMnx cache phản hồi HTTP vào ./cache của thư mục đang chạy lệnh; gom về data/.
# Tải dở thì lần sau dùng lại các phần đã có trong cache này.
ox.settings.cache_folder = settings.graph_cache_file.parent / "osmnx_cache"
# Bản đồ cả thành phố được chia thành vài chục truy vấn Overpass gửi lần lượt, mỗi truy vấn có thể lâu.
# Bỏ bước hỏi /api/status (hay bị treo, mỗi lần chờ 60 giây); gặp lỗi 429 thì OSMnx tự chờ rồi gửi lại.
ox.settings.requests_timeout = 300
ox.settings.overpass_rate_limit = False
if settings.overpass_url:
    ox.settings.overpass_url = settings.overpass_url

# Máy chủ Overpass hay trả 502/504 hoặc không kết nối được khi quá tải
DOWNLOAD_ATTEMPTS = 10
RETRY_PAUSE_S = 30


def boundary_polygon():
    """Ranh giới của PLACE_NAME (lấy từ Nominatim), nới thêm GRAPH_BUFFER_KM."""
    polygon = ox.geocode_to_gdf(settings.place_name).geometry.iloc[0]
    if not settings.graph_buffer_km:
        return polygon
    # Đổi sang hệ tọa độ mét (UTM) để nới đúng số km rồi đổi lại kinh độ, vĩ độ
    projected, crs = ox.projection.project_geometry(polygon)
    buffered = projected.buffer(settings.graph_buffer_km * 1000)
    return ox.projection.project_geometry(buffered, crs=crs, to_latlong=True)[0]


def _download_once() -> nx.MultiDiGraph:
    if settings.graph_bbox:
        west, south, east, north = (float(v) for v in settings.graph_bbox.split(","))
        logger.info("Tải bản đồ theo bbox %s", settings.graph_bbox)
        return ox.graph_from_bbox((west, south, east, north), network_type="drive")
    logger.info("Tải bản đồ theo tên: %s", settings.map_name)
    return ox.graph_from_polygon(boundary_polygon(), network_type="drive")


def download_graph() -> nx.MultiDiGraph:
    """Tải mạng đường cho ô tô từ OpenStreetMap theo bbox (nếu có) hoặc theo tên khu vực.

    Lỗi mạng thì thử lại; các phần đã tải xong nằm trong cache nên không phải tải lại.
    """
    for attempt in range(1, DOWNLOAD_ATTEMPTS):
        try:
            return _download_once()
        except (requests.RequestException, ResponseStatusCodeError) as e:
            logger.warning("Tải lỗi lần %d/%d: %s. Thử lại sau %d giây", attempt, DOWNLOAD_ATTEMPTS, e, RETRY_PAUSE_S)
            time.sleep(RETRY_PAUSE_S)
    return _download_once()


def load_graph_file() -> nx.MultiDiGraph:
    """Đọc đồ thị từ file cache; chưa có thì tải từ mạng rồi lưu lại."""
    path = settings.graph_cache_file
    if path.exists():
        logger.info("Đọc bản đồ từ cache %s", path)
        return ox.load_graphml(path)

    G = download_graph()
    path.parent.mkdir(parents=True, exist_ok=True)
    ox.save_graphml(G, path)
    logger.info("Đã lưu cache %s", path)
    return G


def load_graph(db: sessionmaker | None = None) -> tuple[nx.MultiDiGraph, int | None]:
    """Trả về (đồ thị, id bản đồ trong database).

    Có database: đọc từ bảng nodes, edges; lần đầu thì lấy từ file/OSM rồi lưu vào database.
    Không có database: chỉ dùng file cache, id bản đồ là None.
    """
    map_id = None
    if db is None:
        G = load_graph_file()
    else:
        with db() as session:
            found = repository.load_graph(session, settings.map_name)
            if found:
                logger.info("Đọc bản đồ từ database: %s", settings.map_name)
                map_id, G = found
            else:
                G = load_graph_file()
                map_id = repository.save_graph(session, settings.map_name, G)
                logger.info("Đã lưu bản đồ vào database, map_id=%s", map_id)

    # Đường bị cắt ở ranh giới khu vực để lại những node một chiều chỉ đi vào hoặc chỉ đi ra.
    # Với TP.HCM mới, bước này cũng bỏ Côn Đảo vì không nối đường bộ với đất liền.
    # Giữ thành phần liên thông mạnh lớn nhất để giữa 2 node bất kỳ luôn có đường đi.
    return ox.truncate.largest_component(G, strongly=True), map_id


def graph_info(G: nx.MultiDiGraph) -> dict:
    """Số node, số cạnh, khung bao [south, west, north, east] và tâm [lat, lng]."""
    lats = [data["y"] for _, data in G.nodes(data=True)]
    lngs = [data["x"] for _, data in G.nodes(data=True)]
    south, north = min(lats), max(lats)
    west, east = min(lngs), max(lngs)
    return {
        "place_name": settings.place_name,
        "node_count": G.number_of_nodes(),
        "edge_count": G.number_of_edges(),
        "bbox": [south, west, north, east],
        "center": [(south + north) / 2, (west + east) / 2],
    }
