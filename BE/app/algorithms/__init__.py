# Danh sách thuật toán, dùng chung cho API tìm đường và benchmark
from app.algorithms.astar import astar
from app.algorithms.dijkstra import dijkstra

ALGORITHMS = {"dijkstra": dijkstra, "astar": astar}

# Thời gian chạy chỉ vài ms nên dễ nhiễu; chạy lại vài lần, lấy lần nhanh nhất (cách timeit đo)
TIMING_REPEATS = 5


def run_algorithm(name: str, G, start, goal) -> dict:
    runs = [ALGORITHMS[name](G, start, goal) for _ in range(TIMING_REPEATS)]
    return min(runs, key=lambda r: r["runtime_ms"])
