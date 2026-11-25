import pytest
from fastapi.testclient import TestClient

from app.algorithms.utils import NoPathError
from app.api import routes
from app.main import app
from tests.test_api import client as route_client
from tests.test_api import route_params

client = route_client


def test_compare_reuses_route_results(client):
    response = client.get("/api/compare", params=route_params())
    assert response.status_code == 200
    expected = [
        client.get("/api/route", params=route_params(algo=name)).json()
        for name in ("dijkstra", "astar")
    ]
    assert response.json() == {"results": expected}


@pytest.mark.parametrize(
    ("params", "status"),
    [
        (route_params(to_lat=91), 422),
        (route_params(to_lat=21.03), 400),
        (route_params(from_lat=10.780, from_lng=106.700, to_lat=10.770, to_lng=106.690), 404),
    ],
)
def test_compare_errors(client, params, status):
    assert client.get("/api/compare", params=params).status_code == status


def test_benchmark_is_seeded_and_summarizes_complete_pairs(client, monkeypatch):
    monkeypatch.setattr(
        routes, "haversine", lambda a_lat, _a_lng, b_lat, _b_lng: (b_lat - a_lat) * 100_000
    )
    params = {"n": 5, "seed": 11}
    response = client.get("/api/benchmark", params=params)
    assert response.status_code == 200
    result = response.json()
    assert result == client.get("/api/benchmark", params=params).json()
    assert result["pair_count"] == 5
    assert len(result["rows"]) == 10
    for pair in range(5):
        first, second = result["rows"][pair * 2:pair * 2 + 2]
        assert first["pair"] == second["pair"] == pair
        assert (first["algorithm"], second["algorithm"]) == ("dijkstra", "astar")
        assert first["straight_m"] == second["straight_m"] > 0
        assert first["distance_m"] == second["distance_m"] > 0

    for summary in result["summary"]:
        rows = [row for row in result["rows"] if row["algorithm"] == summary["algorithm"]]
        for metric in ("distance_m", "runtime_ms", "visited_count"):
            assert summary[f"avg_{metric}"] == sum(row[metric] for row in rows) / 5


@pytest.mark.parametrize("node_count", [1, 3])
def test_benchmark_without_reachable_pairs_is_bounded(client, monkeypatch, node_count):
    calls = []

    def no_route(_name, _graph, _start, _goal):
        calls.append(1)
        raise NoPathError

    monkeypatch.setattr(routes, "run_algorithm", no_route)
    graph = app.state.graph
    graph.remove_nodes_from(list(graph.nodes)[node_count:])
    response = client.get("/api/benchmark", params={"n": 2})
    assert response.status_code == 200
    assert response.json() == {"pair_count": 0, "summary": [], "rows": []}
    assert len(calls) == (20 if node_count > 1 else 0)


@pytest.mark.parametrize("params", [{"n": 0}, {"n": 501}, {"n": 3.5}, {"seed": "abc"}])
def test_benchmark_rejects_invalid_query(client, params):
    assert client.get("/api/benchmark", params=params).status_code == 422


def test_comparison_endpoints_require_graph(monkeypatch):
    monkeypatch.setattr(app.state, "graph", None, raising=False)
    client = TestClient(app)
    assert client.get("/api/compare", params=route_params()).status_code == 503
    assert client.get("/api/benchmark").status_code == 503


def test_comparison_endpoints_report_unimplemented_algorithms(client, monkeypatch):
    def unimplemented(*_args):
        raise NotImplementedError

    monkeypatch.setattr(routes, "run_algorithm", unimplemented)
    assert client.get("/api/compare", params=route_params()).status_code == 503
    assert client.get("/api/benchmark").status_code == 503
