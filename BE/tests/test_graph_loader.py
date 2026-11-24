import networkx as nx
import osmnx as ox
import pytest
from fastapi.testclient import TestClient

from app.algorithms.utils import nearest_node
from app.config import settings
from app.graph_loader import graph_info, load_graph
from app.main import app


@pytest.fixture
def road_graph():
    graph = nx.MultiDiGraph(crs="epsg:4326", simplified=True)
    graph.add_node(1, y=10.770, x=106.690)
    graph.add_node(2, y=10.780, x=106.700)
    graph.add_node(3, y=10.785, x=106.705)
    graph.add_edge(1, 2, length=1600.0)
    graph.add_edge(1, 2, length=1750.0)
    graph.add_edge(2, 1, length=1600.0)
    graph.add_edge(2, 3, length=800.0)
    return graph


def test_load_graph_downloads_only_when_needed(tmp_path, monkeypatch, road_graph):
    cache_file = tmp_path / "data" / "graph.graphml"
    calls = []

    def download(place_name, *, network_type):
        calls.append((place_name, network_type))
        return road_graph.copy()

    monkeypatch.setattr(ox.settings, "cache_folder", ox.settings.cache_folder)
    monkeypatch.setattr(ox.graph, "graph_from_place", download)

    for place_name in ("Khu vực A", "Khu vực A", "Khu vực B"):
        graph = load_graph(place_name, cache_file)
        assert set(graph.nodes) == {1, 2}
        assert graph.number_of_edges() == 3
        assert graph[1][2][0]["length"] == 1600.0

    assert cache_file.is_file()
    assert calls == [("Khu vực A", "drive"), ("Khu vực B", "drive")]


def test_graph_info(road_graph):
    graph = ox.truncate.largest_component(road_graph, strongly=True)
    info = graph_info(graph, "Khu vực A")

    assert info["place_name"] == "Khu vực A"
    assert info["node_count"] == 2
    assert info["edge_count"] == 3
    assert info["bbox"] == [10.770, 106.690, 10.780, 106.700]
    assert info["center"] == pytest.approx([10.775, 106.695])


def test_nearest_node_uses_geographic_distance():
    graph = nx.MultiDiGraph()
    graph.add_node(1, y=80.0, x=0.2)
    graph.add_node(2, y=80.1, x=0.0)

    assert nearest_node(graph, 80.0, 0.0) == 1


def test_api_loads_graphml_at_startup(tmp_path, monkeypatch, road_graph):
    cache_file = tmp_path / "graph.graphml"
    ox.io.save_graphml(road_graph, cache_file)
    monkeypatch.setattr(settings, "graph_cache_path", str(cache_file))
    monkeypatch.setattr(settings, "place_name", "Khu vực kiểm thử")
    monkeypatch.setattr(app.state, "graph", None, raising=False)
    monkeypatch.setattr(app.state, "graph_info", None, raising=False)

    with TestClient(app) as client:
        response = client.get("/api/graph/info")
        assert response.status_code == 200
        info = response.json()
        assert info["place_name"] == "Khu vực kiểm thử"
        assert info["node_count"] == 2
        assert info["edge_count"] == 3
        assert info["bbox"] == [10.770, 106.690, 10.780, 106.700]
        assert info["center"] == pytest.approx([10.775, 106.695])
