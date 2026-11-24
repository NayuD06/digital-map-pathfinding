
"""Thuật toán A* với heuristic Haversine."""

import heapq
import math
import time
from itertools import count

from app.algorithms.utils import (
    NoPathError,
    haversine,
    neighbors,
    reconstruct_path,
)


def astar(G, start, goal) -> dict:
    t0 = time.perf_counter()

    if start not in G or goal not in G:
        raise NoPathError("Node bắt đầu hoặc kết thúc không tồn tại")

    goal_lat = G.nodes[goal]["y"]
    goal_lng = G.nodes[goal]["x"]

    def heuristic(node):
        return haversine(
            G.nodes[node]["y"],
            G.nodes[node]["x"],
            goal_lat,
            goal_lng,
        )

    g = {start: 0.0}
    parent = {}
    visited = set()
    visited_order = []

    counter = count()
    heap = [
        (heuristic(start), next(counter), start)
    ]

    while heap:
        _, _, u = heapq.heappop(heap)

        if u in visited:
            continue

        visited.add(u)
        visited_order.append(u)

        if u == goal:
            break

        for v, w in neighbors(G, u):
            new_g = g[u] + w

            if new_g < g.get(v, math.inf):
                g[v] = new_g
                parent[v] = u

                f = new_g + heuristic(v)

                heapq.heappush(
                    heap,
                    (f, next(counter), v),
                )

    if goal not in visited:
        raise NoPathError(
            f"Không có đường từ {start} tới {goal}"
        )

    path = reconstruct_path(parent, start, goal)

    return {
        "path": path,
        "distance_m": float(g[goal]),
        "visited_count": len(visited_order),
        "visited_nodes": visited_order,
        "runtime_ms": (time.perf_counter() - t0) * 1000,
    }
