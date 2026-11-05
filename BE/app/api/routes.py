# Các endpoint: GET /api/graph/info, /api/route, /api/compare, /api/history; POST /api/benchmark
import logging
import random
from typing import Annotated, get_args

from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy.exc import SQLAlchemyError

from app import repository
from app.algorithms import run_algorithm
from app.algorithms.utils import NoPathError, nearest_node
from app.benchmark import run_benchmark, summarize
from app.schemas import (
    Algorithm,
    BenchmarkResponse,
    CompareResult,
    GraphInfo,
    HistoryItem,
    RouteResult,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

# Tuyến dài trên bản đồ cả thành phố duyệt hàng trăm nghìn node; chỉ gửi một phần cho FE vẽ
MAX_VISITED_SHOWN = 5000


def _sample(nodes: list, limit: int) -> list:
    """Lấy đều tối đa `limit` phần tử, giữ thứ tự duyệt."""
    if len(nodes) <= limit:
        return nodes
    step = len(nodes) / limit
    return [nodes[int(i * step)] for i in range(limit)]


def _snap(request: Request, lat: float, lng: float):
    """Kiểm tra tọa độ nằm trong khung bao của bản đồ rồi trả về node gần nhất."""
    south, west, north, east = request.app.state.graph_info["bbox"]
    if not (south <= lat <= north and west <= lng <= east):
        raise HTTPException(400, f"Tọa độ ({lat}, {lng}) nằm ngoài vùng bản đồ")
    return nearest_node(request.app.state.graph, lat, lng)


def _save_history(request: Request, algo: str, points: tuple, start, goal, result: dict) -> None:
    """Ghi lịch sử vào database. Lỗi database không làm hỏng kết quả tìm đường."""
    db = request.app.state.db
    if db is None:
        return
    from_lat, from_lng, to_lat, to_lng = points
    try:
        with db() as session:
            repository.save_route_query(
                session,
                map_id=request.app.state.map_id,
                algorithm=algo,
                from_lat=from_lat,
                from_lng=from_lng,
                to_lat=to_lat,
                to_lng=to_lng,
                start_node=start,
                goal_node=goal,
                distance_m=result["distance_m"],
                runtime_ms=result["runtime_ms"],
                visited_count=result["visited_count"],
            )
    except SQLAlchemyError as e:
        logger.warning("Không lưu được lịch sử: %s", e)


def _run(request: Request, algo: str, points: tuple) -> RouteResult:
    from_lat, from_lng, to_lat, to_lng = points
    start = _snap(request, from_lat, from_lng)
    goal = _snap(request, to_lat, to_lng)
    G = request.app.state.graph
    try:
        result = run_algorithm(algo, G, start, goal)
    except NoPathError as e:
        raise HTTPException(404, "Không có đường đi giữa 2 điểm đã chọn") from e

    _save_history(request, algo, points, start, goal, result)

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


@router.get("/graph/info", response_model=GraphInfo)
def get_graph_info(request: Request):
    return request.app.state.graph_info


@router.get("/route", response_model=RouteResult)
def get_route(
    request: Request,
    from_lat: float,
    from_lng: float,
    to_lat: float,
    to_lng: float,
    algo: Algorithm = "astar",
):
    return _run(request, algo, (from_lat, from_lng, to_lat, to_lng))


@router.get("/compare", response_model=CompareResult)
def get_compare(request: Request, from_lat: float, from_lng: float, to_lat: float, to_lng: float):
    points = (from_lat, from_lng, to_lat, to_lng)
    return {"results": [_run(request, algo, points) for algo in get_args(Algorithm)]}


@router.get("/history", response_model=list[HistoryItem])
def get_history(request: Request, limit: Annotated[int, Query(ge=1, le=100)] = 20):
    db = request.app.state.db
    if db is None:
        raise HTTPException(503, "Chưa cấu hình database nên không có lịch sử")
    with db() as session:
        return repository.recent_route_queries(session, request.app.state.map_id, limit)


@router.post("/benchmark", response_model=BenchmarkResponse)
def post_benchmark(
    request: Request,
    n: Annotated[int, Query(ge=1, le=500, description="Số cặp điểm ngẫu nhiên")] = 50,
    seed: Annotated[int | None, Query(description="Cùng seed thì ra cùng các cặp điểm")] = None,
):
    if seed is None:
        seed = random.randrange(1_000_000)
    rows = run_benchmark(request.app.state.graph, n, seed)
    stats = summarize(rows)

    run_id = None
    db = request.app.state.db
    if db is not None:
        try:
            with db() as session:
                run_id = repository.save_benchmark(
                    session, request.app.state.map_id, seed, stats["pair_count"], rows
                )
        except SQLAlchemyError as e:
            logger.warning("Không lưu được kết quả benchmark: %s", e)

    return {"run_id": run_id, "seed": seed, "rows": rows, **stats}
