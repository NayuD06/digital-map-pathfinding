# Hàm tiện ích: haversine, dựng lại đường đi từ bảng parent, tìm node gần nhất
import math
import time

# Nhỏ hơn bán kính OSMnx dùng (6 371 009 m) để heuristic không bao giờ ước lượng quá
EARTH_RADIUS_M = 6_371_000


class NoPathError(Exception):
    """Không có đường đi từ điểm đầu tới điểm cuối."""


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Khoảng cách đường tròn lớn giữa 2 tọa độ, đơn vị mét."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = phi2 - phi1
    d_lambda = math.radians(lng2 - lng1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(a))


def node_distance(G, u, v) -> float:
    """Khoảng cách đường chim bay giữa 2 node (thuộc tính y = lat, x = lng)."""
    a, b = G.nodes[u], G.nodes[v]
    return haversine(a["y"], a["x"], b["y"], b["x"])


def neighbors(G, u):
    """Sinh (v, độ dài) cho mỗi cạnh u → v.

    Đồ thị OSMnx là MultiDiGraph nên giữa 2 node có thể có nhiều cạnh song song,
    khi đó lấy cạnh ngắn nhất.
    """
    multi = G.is_multigraph()
    for v, data in G[u].items():
        if multi:
            yield v, min(edge["length"] for edge in data.values())
        else:
            yield v, data["length"]


def reconstruct_path(parent: dict, start, goal) -> list:
    """Lần ngược bảng parent từ goal về start."""
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def nearest_node(G, lat: float, lng: float):
    """Node gần tọa độ nhất. Duyệt hết node, đủ nhanh với đồ thị cỡ một quận."""
    return min(G.nodes, key=lambda n: haversine(lat, lng, G.nodes[n]["y"], G.nodes[n]["x"]))


def build_result(parent: dict, dist: dict, visited_order: list, start, goal, started_at: float) -> dict:
    """Cấu trúc kết quả chung của mọi thuật toán."""
    if goal not in dist:
        raise NoPathError(f"Không có đường đi từ {start} tới {goal}")
    path = reconstruct_path(parent, start, goal)
    return {
        "path": path,
        "distance_m": dist[goal],
        "visited_count": len(visited_order),
        "visited_nodes": visited_order,
        "runtime_ms": (time.perf_counter() - started_at) * 1000,
    }
