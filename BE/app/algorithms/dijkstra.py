
"""Thuật toán Dijkstra sử dụng hàng đợi ưu tiên."""

import heapq
import math
import time
from itertools import count

from app.algorithms.utils import (
    NoPathError,
    neighbors,
    reconstruct_path,
)


def dijkstra(G, start, goal) -> dict:
    t0 = time.perf_counter()

    if start not in G or goal not in G:
        raise NoPathError("Node bắt đầu hoặc kết thúc không tồn tại")

    dist = {start: 0.0}
    parent = {}
    visited = set()
    visited_order = []

    counter = count()
    heap = [(0.0, next(counter), start)]

    while heap:
        d, _, u = heapq.heappop(heap)

        # Bỏ qua bản ghi cũ trong heap.
        if u in visited:
            continue

        visited.add(u)
        visited_order.append(u)

        # Đã xác định đường đi ngắn nhất tới đích.
        if u == goal:
            break

        # Nới lỏng các cạnh đi ra từ u.
        for v, w in neighbors(G, u):
            nd = d + w

            if nd < dist.get(v, math.inf):
                dist[v] = nd
                parent[v] = u

                heapq.heappush(
                    heap,
                    (nd, next(counter), v),
                )

    if goal not in visited:
        raise NoPathError(
            f"Không có đường từ {start} tới {goal}"
        )

    path = reconstruct_path(parent, start, goal)

    return {
        "path": path,
        "distance_m": float(dist[goal]),
        "visited_count": len(visited_order),
        "visited_nodes": visited_order,
        "runtime_ms": (time.perf_counter() - t0) * 1000,
    }
