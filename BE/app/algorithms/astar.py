# Cài đặt thuật toán A* với heuristic Haversine
import heapq
import itertools
import time

from app.algorithms.utils import build_result, distance_to, prepare


def astar(G, start, goal) -> dict:
    """Giống Dijkstra nhưng ưu tiên node có f = g + h nhỏ nhất.

    g: độ dài đã đi từ start, h: khoảng cách đường chim bay (Haversine) tới goal.
    Đường thật luôn dài hơn hoặc bằng đường chim bay nên h không bao giờ ước lượng
    quá (chấp nhận được) và thỏa bất đẳng thức tam giác (nhất quán), vì vậy A*
    vẫn cho đường ngắn nhất và mỗi node chỉ cần duyệt một lần.
    """
    prepared = prepare(G)
    adj = prepared.adj
    started_at = time.perf_counter()
    h = distance_to(prepared, goal)
    dist = {start: 0.0}
    parent = {}
    visited = set()
    visited_order = []
    tie = itertools.count()
    heap = [(h(start), next(tie), start)]

    while heap:
        _, _, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        visited_order.append(u)
        if u == goal:
            break

        for v, w in adj[u]:
            g = dist[u] + w
            if g < dist.get(v, float("inf")):
                dist[v] = g
                parent[v] = u
                heapq.heappush(heap, (g + h(v), next(tie), v))

    return build_result(parent, dist, visited_order, start, goal, started_at)
