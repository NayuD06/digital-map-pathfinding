# Hàm tiện ích: haversine, dựng lại đường đi từ bảng parent, tìm node gần nhất
import math
import time
import weakref
from typing import NamedTuple

import numpy as np

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


class PreparedGraph(NamedTuple):
    """Dữ liệu tính sẵn để thuật toán không phải tra NetworkX ở mỗi bước."""

    adj: dict  # u -> [(v, độ dài), ...]
    coords: dict  # node -> (lat radian, lng radian, cos lat)
    ids: list  # id node, cùng thứ tự với các mảng bên dưới
    lat: np.ndarray  # radian
    lng: np.ndarray  # radian
    cos_lat: np.ndarray


_prepared: "weakref.WeakKeyDictionary[object, PreparedGraph]" = weakref.WeakKeyDictionary()


def prepare(G) -> PreparedGraph:
    """Tính một lần cho mỗi đồ thị rồi dùng lại. Sửa đồ thị sau khi đã chạy thuật toán thì phải tạo đồ thị mới."""
    prepared = _prepared.get(G)
    if prepared is None:
        ids = list(G.nodes)
        lat = np.radians([G.nodes[n]["y"] for n in ids])
        lng = np.radians([G.nodes[n]["x"] for n in ids])
        cos_lat = np.cos(lat)
        prepared = PreparedGraph(
            adj={u: list(neighbors(G, u)) for u in ids},
            coords={n: (float(a), float(b), float(c)) for n, a, b, c in zip(ids, lat, lng, cos_lat, strict=True)},
            ids=ids,
            lat=lat,
            lng=lng,
            cos_lat=cos_lat,
        )
        _prepared[G] = prepared
    return prepared


def distance_to(prepared: PreparedGraph, goal):
    """Hàm h(v) = Haversine từ v tới goal, dùng làm heuristic cho A*."""
    lat2, lng2, cos2 = prepared.coords[goal]
    coords = prepared.coords
    sin, asin, sqrt = math.sin, math.asin, math.sqrt

    def h(v) -> float:
        lat1, lng1, cos1 = coords[v]
        a = sin((lat2 - lat1) / 2) ** 2 + cos1 * cos2 * sin((lng2 - lng1) / 2) ** 2
        return 2 * EARTH_RADIUS_M * asin(sqrt(min(a, 1.0)))

    return h


def reconstruct_path(parent: dict, start, goal) -> list:
    """Lần ngược bảng parent từ goal về start."""
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def nearest_node(G, lat: float, lng: float):
    """Node gần tọa độ nhất, tính Haversine cho mọi node cùng lúc bằng numpy."""
    p = prepare(G)
    phi, lam = math.radians(lat), math.radians(lng)
    # Chỉ cần so sánh nên bỏ qua bước asin/sqrt (đơn điệu)
    a = np.sin((p.lat - phi) / 2) ** 2 + math.cos(phi) * p.cos_lat * np.sin((p.lng - lam) / 2) ** 2
    return p.ids[int(np.argmin(a))]


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
