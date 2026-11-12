# Các endpoint: GET /api/graph/info, GET /api/route
# (GET /api/compare, /api/benchmark do TV5 thêm vào file này, dùng lại hàm find_route bên dưới)
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request

from app.algorithms import run_algorithm
from app.algorithms.utils import NoPathError, nearest_node
from app.schemas import Algorithm, ErrorResponse, GraphInfo, RouteQuery, RouteResult

router = APIRouter(prefix="/api")

# Tuyến dài có thể duyệt rất nhiều node; chỉ gửi tối đa chừng này điểm cho FE vẽ
MAX_VISITED_SHOWN = 5000

ERRORS = {
    400: {"model": ErrorResponse, "description": "Tọa độ nằm ngoài vùng bản đồ"},
    404: {"model": ErrorResponse, "description": "Không có đường đi giữa 2 điểm"},
    503: {"model": ErrorResponse, "description": "Server chưa nạp bản đồ"},
}


def _sample(items: list, limit: int) -> list:
    """Lấy đều tối đa `limit` phần tử, giữ nguyên thứ tự duyệt."""
    if len(items) <= limit:
        return items
    step = len(items) / limit
    return [items[int(i * step)] for i in range(limit)]


def _graph(request: Request):
    G = getattr(request.app.state, "graph", None)
    if G is None:
        raise HTTPException(503, "Server chưa nạp bản đồ")
    return G


def _snap(request: Request, lat: float, lng: float):
    """Kiểm tra tọa độ nằm trong khung bao bản đồ rồi trả về node gần nhất."""
    south, west, north, east = request.app.state.graph_info["bbox"]
    if not (south <= lat <= north and west <= lng <= east):
        raise HTTPException(400, f"Tọa độ ({lat}, {lng}) nằm ngoài vùng bản đồ")
    return nearest_node(request.app.state.graph, lat, lng)


def find_route(
    request: Request, algo: Algorithm, from_lat: float, from_lng: float, to_lat: float, to_lng: float
) -> RouteResult:
    """Tìm đường giữa 2 tọa độ và đổi kết quả của thuật toán sang định dạng API."""
    G = _graph(request)
    start = _snap(request, from_lat, from_lng)
    goal = _snap(request, to_lat, to_lng)
    try:
        result = run_algorithm(algo, G, start, goal)
    except NoPathError as e:
        raise HTTPException(404, "Không có đường đi giữa 2 điểm đã chọn") from e

    def coords(nodes):
        return [[G.nodes[n]["y"], G.nodes[n]["x"]] for n in nodes]

    return RouteResult(
        algorithm=algo,
        path=coords(result["path"]),
        visited=coords(_sample(result["visited_nodes"], MAX_VISITED_SHOWN)),
        distance_m=result["distance_m"],
        runtime_ms=result["runtime_ms"],
        visited_count=result["visited_count"],
    )


@router.get("/graph/info", response_model=GraphInfo, responses={503: ERRORS[503]})
def get_graph_info(request: Request):
    _graph(request)
    return request.app.state.graph_info


@router.get("/route", response_model=RouteResult, responses=ERRORS)
def get_route(request: Request, q: Annotated[RouteQuery, Query()]):
    return find_route(request, q.algo, q.from_lat, q.from_lng, q.to_lat, q.to_lng)
