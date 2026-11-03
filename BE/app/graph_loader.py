# Tải mạng đường của quận bằng OSMnx; lưu vào MySQL nếu có, cache .graphml trong thư mục data/
import logging

import networkx as nx
import osmnx as ox
from sqlalchemy.orm import sessionmaker

from app import repository
from app.config import settings

logger = logging.getLogger(__name__)

# Mặc định OSMnx cache phản hồi HTTP vào ./cache của thư mục đang chạy lệnh; gom về data/
ox.settings.cache_folder = settings.graph_cache_file.parent / "osmnx_cache"


def download_graph() -> nx.MultiDiGraph:
    """Tải mạng đường cho ô tô từ OpenStreetMap theo bbox (nếu có) hoặc theo tên quận."""
    if settings.graph_bbox:
        west, south, east, north = (float(v) for v in settings.graph_bbox.split(","))
        logger.info("Tải bản đồ theo bbox %s", settings.graph_bbox)
        return ox.graph_from_bbox((west, south, east, north), network_type="drive")
    logger.info("Tải bản đồ theo tên: %s", settings.place_name)
    return ox.graph_from_place(settings.place_name, network_type="drive")


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

    # Đường bị cắt ở ranh giới quận để lại những node một chiều chỉ đi vào hoặc chỉ đi ra.
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
