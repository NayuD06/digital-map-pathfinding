# Pydantic models cho request/response của API tìm đường.
# Đây là định dạng API đã chốt: FE (client.js, dữ liệu giả) và BE cùng theo file này.
# Muốn đổi thì báo cả nhóm và sửa cả FE.
from typing import Literal

from pydantic import BaseModel, Field

Algorithm = Literal["dijkstra", "astar"]


class GraphInfo(BaseModel):
    """GET /api/graph/info"""

    place_name: str
    node_count: int
    edge_count: int
    bbox: list[float] = Field(description="[south, west, north, east]")
    center: list[float] = Field(description="[lat, lng]")


class RouteQuery(BaseModel):
    """Tham số của GET /api/route (query string)."""

    algo: Algorithm = "astar"
    from_lat: float = Field(ge=-90, le=90)
    from_lng: float = Field(ge=-180, le=180)
    to_lat: float = Field(ge=-90, le=90)
    to_lng: float = Field(ge=-180, le=180)


class RouteResult(BaseModel):
    """GET /api/route"""

    algorithm: Algorithm
    path: list[list[float]] = Field(description="Tọa độ đường đi [[lat, lng], ...]")
    visited: list[list[float]] = Field(description="Tọa độ node đã duyệt [[lat, lng], ...], theo thứ tự duyệt")
    distance_m: float = Field(description="Độ dài đường đi (mét)")
    runtime_ms: float = Field(description="Thời gian chạy thuật toán (mili giây)")
    visited_count: int = Field(description="Tổng số node đã duyệt")


class CompareResult(BaseModel):
    """GET /api/compare: kết quả của từng thuật toán trên cùng cặp điểm."""

    results: list[RouteResult]


class ErrorResponse(BaseModel):
    """Lỗi 400 (tọa độ ngoài bản đồ), 404 (không có đường), 503 (chưa nạp bản đồ)."""

    detail: str
