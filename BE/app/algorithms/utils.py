
"""Các hàm tiện ích cho thuật toán tìm đường."""

import math

from osmnx.distance import great_circle

EARTH_RADIUS_M = 6_371_000


class NoPathError(Exception):
    """Không có đường đi giữa 2 node. API đổi thành HTTP 404."""


def haversine(
    lat1: float,
    lng1: float,
    lat2: float,
    lng2: float,
) -> float:
    """Tính khoảng cách đường chim bay, đơn vị mét."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(d_lambda / 2) ** 2
    )

    # Tránh lỗi do sai số số thực.
    a = max(0.0, min(1.0, a))

    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(a))


def reconstruct_path(parent: dict, start, goal) -> list:
    """Dựng lại đường đi từ start tới goal."""
    path = [goal]

    while path[-1] != start:
        path.append(parent[path[-1]])

    path.reverse()

    return path


def neighbors(G, u):
    """Trả về node kề và trọng số cạnh ngắn nhất."""
    for v, edges in G[u].items():
        if G.is_multigraph():
            length = min(
                edge["length"]
                for edge in edges.values()
            )
        else:
            length = edges["length"]

        yield v, float(length)


def nearest_node(G, lat: float, lng: float):
    """Tìm ID node gần tọa độ nhất (phần của TV2)."""
    return min(
        G.nodes,
        key=lambda node: great_circle(
            lat,
            lng,
            G.nodes[node]["y"],
            G.nodes[node]["x"],
        ),
    )
