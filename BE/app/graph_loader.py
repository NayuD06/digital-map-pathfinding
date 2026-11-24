"""Tải và lưu đồ thị đường ô tô từ OpenStreetMap."""

import logging
from pathlib import Path
from tempfile import NamedTemporaryFile

import osmnx as ox

logger = logging.getLogger(__name__)


def load_graph(place_name: str, cache_file: Path):
    """Trả về thành phần liên thông mạnh lớn nhất của mạng đường đã chọn."""
    graph = None
    if cache_file.is_file():
        cached_graph = ox.io.load_graphml(cache_file)
        # Các file GraphML cũ có thể chưa lưu tên địa danh trong metadata.
        if cached_graph.graph.get("cache_place_name", place_name) == place_name:
            logger.info("Đọc bản đồ từ %s", cache_file)
            graph = cached_graph

    if graph is None:
        ox.settings.cache_folder = cache_file.parent / "osmnx_cache"
        logger.info("Nạp mạng đường %s qua OSMnx", place_name)
        graph = ox.graph.graph_from_place(place_name, network_type="drive")
        if not graph:
            raise ValueError(f"Không có nút đường ô tô cho {place_name}")

        graph.graph["cache_place_name"] = place_name
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        # Chỉ thay cache sau khi đã ghi xong GraphML để lần khởi động sau đọc được.
        with NamedTemporaryFile(dir=cache_file.parent, suffix=".tmp", delete=False) as temp:
            temp_path = Path(temp.name)
        try:
            ox.io.save_graphml(graph, temp_path)
            temp_path.replace(cache_file)
        finally:
            temp_path.unlink(missing_ok=True)

    if not graph:
        raise ValueError(f"Không có nút đường ô tô cho {place_name}")

    component = ox.truncate.largest_component(graph, strongly=True)
    logger.info(
        "Mạng đường: %d nút, %d cạnh trước lọc; %d nút, %d cạnh sau lọc",
        graph.number_of_nodes(),
        graph.number_of_edges(),
        component.number_of_nodes(),
        component.number_of_edges(),
    )
    return component


def graph_info(G, place_name: str) -> dict:
    """Tính số nút, số cạnh, khung bao và tâm khung bao theo định dạng API."""
    latitudes = [data["y"] for _, data in G.nodes(data=True)]
    longitudes = [data["x"] for _, data in G.nodes(data=True)]
    south, north = min(latitudes), max(latitudes)
    west, east = min(longitudes), max(longitudes)
    return {
        "place_name": place_name,
        "node_count": G.number_of_nodes(),
        "edge_count": G.number_of_edges(),
        "bbox": [south, west, north, east],
        "center": [(south + north) / 2, (west + east) / 2],
    }
