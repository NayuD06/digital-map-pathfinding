# Chọn thuật toán theo tên. routes.py chỉ gọi run_algorithm, không gọi trực tiếp từng thuật toán.
from app.algorithms.astar import astar
from app.algorithms.dijkstra import dijkstra

ALGORITHMS = {
    "dijkstra": dijkstra,
    "astar": astar,
}


def run_algorithm(name: str, G, start, goal) -> dict:
    """Chạy thuật toán `name` từ node `start` tới node `goal`.

    Mọi thuật toán trả về cùng một cấu trúc:
        {
            "path": [node_id, ...],
            "distance_m": float,
            "visited_count": int,
            "visited_nodes": [node_id, ...],   # theo thứ tự duyệt
            "runtime_ms": float,
        }
    Không có đường đi thì ném NoPathError (app.algorithms.utils).
    """
    return ALGORITHMS[name](G, start, goal)
