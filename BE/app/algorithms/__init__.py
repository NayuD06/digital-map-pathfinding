# Danh sách thuật toán, dùng chung cho API tìm đường và benchmark
from app.algorithms.astar import astar
from app.algorithms.dijkstra import dijkstra

ALGORITHMS = {"dijkstra": dijkstra, "astar": astar}

# Thời gian chạy chỉ vài ms nên dễ nhiễu; chạy lại vài lần, lấy lần nhanh nhất (cách timeit đo)
TIMING_REPEATS = 5
# Lần chạy lâu hơn mức này (tuyến dài trên bản đồ cả thành phố) ít nhiễu, không cần chạy lại
REPEAT_BELOW_MS = 100


def run_algorithm(name: str, G, start, goal) -> dict:
    best = ALGORITHMS[name](G, start, goal)
    for _ in range(TIMING_REPEATS - 1):
        if best["runtime_ms"] >= REPEAT_BELOW_MS:
            break
        result = ALGORITHMS[name](G, start, goal)
        if result["runtime_ms"] < best["runtime_ms"]:
            best = result
    return best
