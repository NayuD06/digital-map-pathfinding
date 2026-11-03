# Chạy N cặp điểm ngẫu nhiên, đo từng thuật toán để lấy số liệu cho phần đánh giá thực nghiệm
import random
import statistics

from app.algorithms import ALGORITHMS, run_algorithm
from app.algorithms.utils import NoPathError, node_distance


def run_benchmark(G, n: int, seed: int) -> list[dict]:
    """Mỗi cặp điểm cho ra một dòng cho mỗi thuật toán. Cặp không có đường đi thì bỏ qua."""
    rng = random.Random(seed)
    nodes = list(G.nodes)
    rows = []
    pair_index = 0
    attempts = 0
    while pair_index < n and attempts < n * 10:
        attempts += 1
        start, goal = rng.sample(nodes, 2)
        try:
            results = {name: run_algorithm(name, G, start, goal) for name in ALGORITHMS}
        except NoPathError:
            continue

        straight = node_distance(G, start, goal)
        for name, r in results.items():
            rows.append(
                {
                    "pair_index": pair_index,
                    "algorithm": name,
                    "start_node": start,
                    "goal_node": goal,
                    "straight_m": straight,
                    "distance_m": r["distance_m"],
                    "runtime_ms": r["runtime_ms"],
                    "visited_count": r["visited_count"],
                }
            )
        pair_index += 1
    return rows


def summarize(rows: list[dict]) -> dict:
    """Trung bình theo thuật toán và số cặp A* chạy nhanh hơn Dijkstra."""
    by_algo: dict[str, list[dict]] = {}
    by_pair: dict[int, dict[str, dict]] = {}
    for row in rows:
        by_algo.setdefault(row["algorithm"], []).append(row)
        by_pair.setdefault(row["pair_index"], {})[row["algorithm"]] = row

    summary = [
        {
            "algorithm": algo,
            "avg_distance_m": statistics.mean(r["distance_m"] for r in items),
            "avg_runtime_ms": statistics.mean(r["runtime_ms"] for r in items),
            "median_runtime_ms": statistics.median(r["runtime_ms"] for r in items),
            "avg_visited_count": statistics.mean(r["visited_count"] for r in items),
        }
        for algo, items in by_algo.items()
    ]
    astar_faster = sum(p["astar"]["runtime_ms"] < p["dijkstra"]["runtime_ms"] for p in by_pair.values())
    return {"pair_count": len(by_pair), "astar_faster_count": astar_faster, "summary": summary}
