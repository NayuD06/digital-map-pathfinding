# Cài đặt thuật toán Dijkstra (heapq), trả về đường đi + số node đã duyệt
import heapq
import itertools
import time

from app.algorithms.utils import build_result, prepare


def dijkstra(G, start, goal) -> dict:
    """Tìm đường ngắn nhất theo thuộc tính `length` của cạnh.

    Dừng ngay khi lấy được goal ra khỏi hàng đợi. Node "đã duyệt" là node
    đã được lấy ra khỏi hàng đợi (khoảng cách tới nó đã chốt).
    """
    adj = prepare(G).adj
    started_at = time.perf_counter()
    dist = {start: 0.0}
    parent = {}
    visited = set()
    visited_order = []
    # Bộ đếm để so sánh khi 2 phần tử có cùng khoảng cách
    tie = itertools.count()
    heap = [(0.0, next(tie), start)]

    while heap:
        d, _, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        visited_order.append(u)
        if u == goal:
            break

        for v, w in adj[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, next(tie), v))

    return build_result(parent, dist, visited_order, start, goal, started_at)
