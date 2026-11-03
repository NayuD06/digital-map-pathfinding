# Kiểm tra lưu/đọc bản đồ, lịch sử, benchmark (SQLite trong bộ nhớ, không cần MySQL)
import networkx as nx
import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import OperationalError

from app import db as db_module
from app import repository
from app.algorithms.dijkstra import dijkstra
from app.benchmark import run_benchmark, summarize
from app.db import create_session_factory
from app.models import BenchmarkResult
from tests.test_algorithms import LAT0, LNG0, STEP, make_grid


@pytest.fixture
def db():
    return create_session_factory("sqlite://")


def make_osm_like_graph():
    """Đồ thị giống OSMnx: MultiDiGraph, id node là số nguyên, có cạnh song song, name dạng list."""
    G = nx.MultiDiGraph(crs="epsg:4326")
    G.add_node(101, y=LAT0, x=LNG0, street_count=3)
    G.add_node(102, y=LAT0, x=LNG0 + STEP, street_count=2)
    G.add_node(103, y=LAT0 + STEP, x=LNG0 + STEP, street_count=1)
    G.add_edge(101, 102, key=0, length=120.5, name="Lê Lợi", highway="primary", oneway=False)
    G.add_edge(102, 101, key=0, length=120.5, name="Lê Lợi", highway="primary", oneway=False)
    G.add_edge(101, 102, key=1, length=300.0, name=["Pasteur", "Nam Kỳ Khởi Nghĩa"], highway="secondary", oneway=True)
    G.add_edge(102, 103, key=0, length=110.0, highway="residential", oneway=True, maxspeed="40")
    return G


def test_no_database_configured():
    assert create_session_factory(None) is None
    assert create_session_factory("") is None


def test_mysql_unreachable(monkeypatch):
    """Tạo database phải kết nối vào server chứ chưa chọn database; lỗi kết nối thì trả về None."""
    urls = []

    def fake_create_engine(url, **kwargs):
        urls.append(url)
        raise OperationalError("connect", {}, Exception("server không chạy"))

    monkeypatch.setattr(db_module, "create_engine", fake_create_engine)
    assert create_session_factory("mysql+pymysql://root@localhost/digital_map") is None
    assert urls[0].database is None


def test_graph_roundtrip(db):
    G = make_osm_like_graph()
    with db() as session:
        map_id = repository.save_graph(session, "Quận test", G)

    with db() as session:
        loaded_id, loaded = repository.load_graph(session, "Quận test")

    assert loaded_id == map_id
    assert set(loaded.nodes) == set(G.nodes)
    assert loaded.number_of_edges() == G.number_of_edges()
    assert loaded.nodes[101] == {"y": LAT0, "x": LNG0, "street_count": 3}
    assert loaded[101][102][1]["name"] == "Pasteur, Nam Kỳ Khởi Nghĩa"
    assert loaded[102][103][0]["oneway"] is True
    assert dijkstra(loaded, 101, 103)["distance_m"] == dijkstra(G, 101, 103)["distance_m"]


def test_load_unknown_map(db):
    with db() as session:
        assert repository.load_graph(session, "Không có") is None


def test_route_history_newest_first(db):
    with db() as session:
        map_id = repository.save_graph(session, "Quận test", make_osm_like_graph())
        for i in range(5):
            repository.save_route_query(
                session,
                map_id=map_id,
                algorithm="astar",
                from_lat=LAT0,
                from_lng=LNG0,
                to_lat=LAT0 + STEP,
                to_lng=LNG0 + STEP,
                start_node=101,
                goal_node=103,
                distance_m=100.0 + i,
                runtime_ms=1.0,
                visited_count=3,
            )

    with db() as session:
        items = repository.recent_route_queries(session, map_id, limit=3)

    assert [item.distance_m for item in items] == [104.0, 103.0, 102.0]
    assert items[0].created_at is not None


def test_benchmark_rows_and_summary():
    G = make_grid(10, seed=1)
    rows = run_benchmark(G, n=15, seed=7)

    assert len(rows) == 30
    assert run_benchmark(G, n=15, seed=7)[0]["start_node"] == rows[0]["start_node"]
    for i in range(15):
        dijkstra_row, astar_row = (r for r in rows if r["pair_index"] == i)
        assert dijkstra_row["distance_m"] == pytest.approx(astar_row["distance_m"])
        assert dijkstra_row["distance_m"] >= dijkstra_row["straight_m"]

    stats = summarize(rows)
    assert stats["pair_count"] == 15
    assert 0 <= stats["astar_faster_count"] <= 15
    by_algo = {s["algorithm"]: s for s in stats["summary"]}
    assert by_algo["astar"]["avg_visited_count"] <= by_algo["dijkstra"]["avg_visited_count"]


def test_save_benchmark(db):
    with db() as session:
        map_id = repository.save_graph(session, "Quận test", make_osm_like_graph())
        rows = run_benchmark(make_osm_like_graph(), n=2, seed=0)
        run_id = repository.save_benchmark(session, map_id, seed=0, pair_count=2, rows=rows)

    with db() as session:
        count = session.scalar(select(func.count()).where(BenchmarkResult.run_id == run_id))
    assert count == len(rows)
