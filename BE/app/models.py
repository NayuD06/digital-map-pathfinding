# Các bảng trong database: bản đồ (maps, nodes, edges), lịch sử tìm đường, kết quả benchmark
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Double,
    ForeignKey,
    ForeignKeyConstraint,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Map(Base):
    """Một bản đồ đã tải từ OSM, nhận ra bằng tên quận hoặc bbox."""

    __tablename__ = "maps"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    node_count: Mapped[int]
    edge_count: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Node(Base):
    """Giao lộ hoặc điểm cuối đường. Một node OSM có thể nằm trong nhiều bản đồ nên khóa gồm 2 cột."""

    __tablename__ = "nodes"

    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id", ondelete="CASCADE"), primary_key=True)
    osm_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    lat: Mapped[float] = mapped_column(Double)
    lng: Mapped[float] = mapped_column(Double)
    street_count: Mapped[int | None]


class Edge(Base):
    """Đoạn đường có hướng từ node u tới node v. Đường hai chiều được lưu thành 2 cạnh."""

    __tablename__ = "edges"
    __table_args__ = (
        ForeignKeyConstraint(["map_id", "u"], ["nodes.map_id", "nodes.osm_id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["map_id", "v"], ["nodes.map_id", "nodes.osm_id"], ondelete="CASCADE"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id", ondelete="CASCADE"), index=True)
    u: Mapped[int] = mapped_column(BigInteger)
    v: Mapped[int] = mapped_column(BigInteger)
    # Phân biệt các cạnh song song giữa cùng u, v
    edge_key: Mapped[int]
    length: Mapped[float] = mapped_column(Double, comment="mét")
    name: Mapped[str | None] = mapped_column(String(255))
    highway: Mapped[str | None] = mapped_column(String(64), comment="loại đường theo OSM")
    oneway: Mapped[bool]
    maxspeed: Mapped[str | None] = mapped_column(String(64))


class RouteQuery(Base):
    """Mỗi lần người dùng tìm đường hoặc so sánh (mỗi thuật toán một dòng)."""

    __tablename__ = "route_queries"

    id: Mapped[int] = mapped_column(primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    algorithm: Mapped[str] = mapped_column(String(16))
    from_lat: Mapped[float] = mapped_column(Double)
    from_lng: Mapped[float] = mapped_column(Double)
    to_lat: Mapped[float] = mapped_column(Double)
    to_lng: Mapped[float] = mapped_column(Double)
    start_node: Mapped[int] = mapped_column(BigInteger)
    goal_node: Mapped[int] = mapped_column(BigInteger)
    distance_m: Mapped[float] = mapped_column(Double)
    runtime_ms: Mapped[float] = mapped_column(Double)
    visited_count: Mapped[int]


class BenchmarkRun(Base):
    """Một lần chạy benchmark N cặp điểm ngẫu nhiên."""

    __tablename__ = "benchmark_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    pair_count: Mapped[int]
    seed: Mapped[int]


class BenchmarkResult(Base):
    """Kết quả của một thuật toán trên một cặp điểm trong lần benchmark."""

    __tablename__ = "benchmark_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("benchmark_runs.id", ondelete="CASCADE"), index=True)
    pair_index: Mapped[int]
    algorithm: Mapped[str] = mapped_column(String(16))
    start_node: Mapped[int] = mapped_column(BigInteger)
    goal_node: Mapped[int] = mapped_column(BigInteger)
    # Khoảng cách đường chim bay giữa 2 điểm, để phân tích theo cự ly
    straight_m: Mapped[float] = mapped_column(Double)
    distance_m: Mapped[float] = mapped_column(Double)
    runtime_ms: Mapped[float] = mapped_column(Double)
    visited_count: Mapped[int]
