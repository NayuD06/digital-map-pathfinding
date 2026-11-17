# Tải mạng đường của quận bằng OSMnx, cache ra file .graphml trong thư mục data/
# TV2 cài đặt. main.py gọi 2 hàm dưới đây khi khởi động, giữ nguyên tên hàm và tham số.
from pathlib import Path


def load_graph(place_name: str, cache_file: Path):
    """Đọc đồ thị từ `cache_file` nếu có, không thì tải bằng OSMnx rồi lưu vào đó.

    Trả về networkx.MultiDiGraph; mỗi node có `y` (lat), `x` (lng), mỗi cạnh có `length` (mét).
    """
    raise NotImplementedError("TV2: cài đặt load_graph")


def graph_info(G, place_name: str) -> dict:
    """Thông tin cho GET /api/graph/info, đúng định dạng schemas.GraphInfo:

    {"place_name", "node_count", "edge_count", "bbox": [south, west, north, east], "center": [lat, lng]}
    """
    raise NotImplementedError("TV2: cài đặt graph_info")
