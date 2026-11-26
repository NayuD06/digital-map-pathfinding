
"""Thuật toán Bidirectional Dijkstra."""

import heapq
import math
import time
from itertools import count

from app.algorithms.utils import (
    NoPathError,
    neighbors,
    reconstruct_path,
)


def bidirectional(G, start, goal) -> dict:
    t0 = time.perf_counter()

    if start not in G or goal not in G:
        raise NoPathError("Node bắt đầu hoặc kết thúc không tồn tại")

    if start == goal:
        return {
            "path": [start],
            "distance_m": 0.0,
            "visited_count": 1,
            "visited_nodes": [start],
            "runtime_ms": (time.perf_counter() - t0) * 1000,
        }

    reverse = G.reverse(copy=False) if G.is_directed() else G
    graphs = [G, reverse]

    distances = [
        {start: 0.0},
        {goal: 0.0},
    ]

    parents = [{}, {}]
    settled = [set(), set()]

    visited = set()
    visited_order = []

    serial = count()

    heaps = [
        [(0.0, next(serial), start)],
        [(0.0, next(serial), goal)],
    ]

    best = math.inf
    meeting = None

    def clean(i):
        """Loại bỏ các bản ghi cũ trong heap."""
        while heaps[i]:
            d, _, u = heaps[i][0]

            if u in settled[i] or d != distances[i][u]:
                heapq.heappop(heaps[i])
            else:
                break

    def update(node):
        """Cập nhật tuyến đường tốt nhất giữa hai phía."""
        nonlocal best, meeting

        if node in distances[0] and node in distances[1]:
            candidate = (
                distances[0][node]
                + distances[1][node]
            )

            if candidate < best:
                best = candidate
                meeting = node

    while True:
        clean(0)
        clean(1)

        if not heaps[0] or not heaps[1]:
            break

        # Điều kiện dừng bảo đảm tính tối ưu.
        if heaps[0][0][0] + heaps[1][0][0] >= best:
            break

        # Ưu tiên phía có khoảng cách nhỏ hơn.
        i = 0 if heaps[0][0][0] <= heaps[1][0][0] else 1

        d, _, u = heapq.heappop(heaps[i])
        settled[i].add(u)

        if u not in visited:
            visited.add(u)
            visited_order.append(u)

        update(u)

        for v, w in neighbors(graphs[i], u):
            nd = d + w

            if nd < distances[i].get(v, math.inf):
                distances[i][v] = nd
                parents[i][v] = u

                heapq.heappush(
                    heaps[i],
                    (nd, next(serial), v),
                )

                update(v)

    if meeting is None:
        raise NoPathError(
            f"Không có đường từ {start} tới {goal}"
        )

    # Dựng đường đi từ start đến điểm gặp nhau.
    path = reconstruct_path(
        parents[0],
        start,
        meeting,
    )

    # Nối tiếp từ điểm gặp nhau đến goal.
    u = meeting

    while u != goal:
        u = parents[1][u]
        path.append(u)

    return {
        "path": path,
        "distance_m": float(best),
        "visited_count": len(visited_order),
        "visited_nodes": visited_order,
        "runtime_ms": (time.perf_counter() - t0) * 1000,
    }
