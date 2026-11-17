# Kiểm tra API: /health, /api/graph/info, /api/route với đồ thị nhỏ tự tạo.
# Thuật toán và nearest_node được thay bằng bản giả để test API độc lập với phần của TV2, TV3.
import networkx as nx
import pytest
from fastapi.testclient import TestClient

from app.algorithms.utils import NoPathError
from app.api import routes
from app.main import app

# 3 node trên một đường thẳng: A -> B -> C
NODES = {1: (10.770, 106.690), 2: (10.775, 106.695), 3: (10.780, 106.700)}
INFO = {
    "place_name": "Test",
    "node_count": 3,
    "edge_count": 2,
    "bbox": [10.770, 106.690, 10.780, 106.700],
    "center": [10.775, 106.695],
}


def fake_nearest(G, lat, lng):
    return min(G.nodes, key=lambda n: (G.nodes[n]["y"] - lat) ** 2 + (G.nodes[n]["x"] - lng) ** 2)


def fake_algorithm(name, G, start, goal):
    if goal < start:
        raise NoPathError
    path = list(range(start, goal + 1))
    return {
        "path": path,
        "distance_m": 100.0 * (len(path) - 1),
        "visited_count": len(path),
        "visited_nodes": path,
        "runtime_ms": 0.5,
    }


@pytest.fixture
def client(monkeypatch):
    G = nx.MultiDiGraph()
    for n, (lat, lng) in NODES.items():
        G.add_node(n, y=lat, x=lng)
    G.add_edge(1, 2, length=100.0)
    G.add_edge(2, 3, length=100.0)

    monkeypatch.setattr(routes, "nearest_node", fake_nearest)
    monkeypatch.setattr(routes, "run_algorithm", fake_algorithm)
    # Không dùng `with TestClient(...)` để bỏ qua lifespan (không tải bản đồ thật)
    app.state.graph = G
    app.state.graph_info = INFO
    yield TestClient(app)
    app.state.graph = None
    app.state.graph_info = None


def route_params(**kw):
    params = {"from_lat": 10.770, "from_lng": 106.690, "to_lat": 10.780, "to_lng": 106.700}
    return {**params, **kw}


def test_health():
    assert TestClient(app).get("/health").json() == {"status": "ok"}


def test_graph_info(client):
    assert client.get("/api/graph/info").json() == INFO


@pytest.mark.parametrize("algo", ["dijkstra", "astar"])
def test_route(client, algo):
    res = client.get("/api/route", params=route_params(algo=algo))
    assert res.status_code == 200
    body = res.json()
    assert body["algorithm"] == algo
    assert body["path"] == [list(NODES[n]) for n in (1, 2, 3)]
    assert body["visited"] == body["path"]
    assert body["distance_m"] == 200.0
    assert body["visited_count"] == 3
    assert body["runtime_ms"] == 0.5


def test_route_default_algo_is_astar(client):
    assert client.get("/api/route", params=route_params()).json()["algorithm"] == "astar"


def test_route_invalid_algo(client):
    assert client.get("/api/route", params=route_params(algo="bfs")).status_code == 422


def test_route_missing_param(client):
    params = route_params()
    del params["to_lng"]
    assert client.get("/api/route", params=params).status_code == 422


def test_route_outside_map(client):
    res = client.get("/api/route", params=route_params(to_lat=21.03, to_lng=105.85))
    assert res.status_code == 400
    assert "ngoài vùng bản đồ" in res.json()["detail"]


def test_route_no_path(client):
    # fake_algorithm không có đường khi đi ngược C -> A
    res = client.get(
        "/api/route",
        params=route_params(from_lat=10.780, from_lng=106.700, to_lat=10.770, to_lng=106.690),
    )
    assert res.status_code == 404


def test_visited_is_sampled(client, monkeypatch):
    monkeypatch.setattr(routes, "MAX_VISITED_SHOWN", 2)
    body = client.get("/api/route", params=route_params()).json()
    assert len(body["visited"]) == 2
    assert body["visited_count"] == 3


def test_graph_not_loaded():
    app.state.graph = None
    client = TestClient(app)
    assert client.get("/api/graph/info").status_code == 503
    assert client.get("/api/route", params=route_params()).status_code == 503


def test_cors_allows_frontend():
    res = TestClient(app).get("/health", headers={"Origin": "http://localhost:5173"})
    assert res.headers["access-control-allow-origin"] == "http://localhost:5173"
