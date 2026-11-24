# Hàm tiện ích: haversine, dựng lại đường đi từ bảng parent, tìm node gần nhất
# TV2 cài nearest_node, TV3 cài haversine và reconstruct_path. Giữ nguyên tên hàm và tham số.


from osmnx.distance import great_circle


class NoPathError(Exception):
    """Không có đường đi giữa 2 node. API đổi lỗi này thành HTTP 404."""


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Khoảng cách đường chim bay giữa 2 tọa độ, đơn vị mét."""
    raise NotImplementedError("TV3: cài đặt haversine")


def reconstruct_path(parent: dict, start, goal) -> list:
    """Dựng lại đường đi [start, ..., goal] từ bảng parent."""
    raise NotImplementedError("TV3: cài đặt reconstruct_path")


def nearest_node(G, lat: float, lng: float):
    """Id của node gần tọa độ (lat, lng) nhất. Node có thuộc tính y = lat, x = lng."""
    return min(
        G.nodes,
        key=lambda node: great_circle(lat, lng, G.nodes[node]["y"], G.nodes[node]["x"]),
    )
