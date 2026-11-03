# Pydantic models cho request/response của API tìm đường
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Algorithm = Literal["dijkstra", "astar"]


class GraphInfo(BaseModel):
    place_name: str
    node_count: int
    edge_count: int
    bbox: list[float] = Field(description="[south, west, north, east]")
    center: list[float] = Field(description="[lat, lng]")
    database_enabled: bool = Field(description="Có lưu lịch sử, benchmark vào database không")


class RouteResult(BaseModel):
    algorithm: Algorithm
    path: list[list[float]] = Field(description="Tọa độ đường đi [[lat, lng], ...]")
    visited: list[list[float]] = Field(description="Tọa độ node đã duyệt, theo thứ tự duyệt")
    distance_m: float
    runtime_ms: float
    visited_count: int


class CompareResult(BaseModel):
    results: list[RouteResult]


class HistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    algorithm: Algorithm
    from_lat: float
    from_lng: float
    to_lat: float
    to_lng: float
    distance_m: float
    runtime_ms: float
    visited_count: int


class BenchmarkRow(BaseModel):
    pair_index: int
    algorithm: Algorithm
    start_node: int
    goal_node: int
    straight_m: float = Field(description="Khoảng cách đường chim bay giữa 2 điểm")
    distance_m: float
    runtime_ms: float
    visited_count: int


class BenchmarkSummary(BaseModel):
    algorithm: Algorithm
    avg_distance_m: float
    avg_runtime_ms: float
    median_runtime_ms: float
    avg_visited_count: float


class BenchmarkResponse(BaseModel):
    run_id: int | None = Field(description="Id trong bảng benchmark_runs, None nếu không có database")
    seed: int
    pair_count: int
    astar_faster_count: int
    summary: list[BenchmarkSummary]
    rows: list[BenchmarkRow]
