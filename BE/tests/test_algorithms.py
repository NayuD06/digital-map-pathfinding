# Kiểm tra Dijkstra và A* cho cùng độ dài đường đi trên đồ thị mẫu
import random

import networkx as nx
import pytest

from app.algorithms.astar import astar
from app.algorithms.dijkstra import dijkstra
from app.algorithms.utils import (
    NoPathError,
    haversine,
    nearest_node,
    node_distance,
    reconstruct_path,
)
from app.config import settings

ALGORITHMS = [dijkstra, astar]

# Gốc tọa độ gần Quận 1 để heuristic Haversine có ý nghĩa
LAT0, LNG0 = 10.77, 106.70
STEP = 0.001  # khoảng 110 m


def make_graph(edges, coords, multi=False):
    """Đồ thị có hướng; độ dài cạnh mặc định bằng khoảng cách đường chim bay."""
    G = nx.MultiDiGraph() if multi else nx.DiGraph()
    for n, (lat, lng) in coords.items():
        G.add_node(n, y=lat, x=lng)
    for u, v, *length in edges:
        G.add_edge(u, v, length=length[0] if length else node_distance(G, u, v))
    return G


def make_grid(size, seed):
    """Lưới size x size, hai chiều, độ dài cạnh = khoảng cách thật x hệ số ngẫu nhiên >= 1."""
    rng = random.Random(seed)
    coords = {(r, c): (LAT0 + r * STEP, LNG0 + c * STEP) for r in range(size) for c in range(size)}
    G = make_graph([], coords)
    for r, c in coords:
        for dr, dc in [(0, 1), (1, 0)]:
            nb = (r + dr, c + dc)
            if nb in coords:
                length = node_distance(G, (r, c), nb) * rng.uniform(1.0, 3.0)
                G.add_edge((r, c), nb, length=length)
                G.add_edge(nb, (r, c), length=length)
    return G


def test_haversine_known_distance():
    # 1 độ vĩ ≈ 111.19 km
    assert haversine(10.0, 106.0, 11.0, 106.0) == pytest.approx(111_195, rel=1e-3)
    assert haversine(10.0, 106.0, 10.0, 106.0) == 0


def test_reconstruct_path():
    assert reconstruct_path({"b": "a", "c": "b"}, "a", "c") == ["a", "b", "c"]
    assert reconstruct_path({}, "a", "a") == ["a"]


def test_nearest_node():
    G = make_grid(3, seed=0)
    assert nearest_node(G, LAT0 + 1.1 * STEP, LNG0 + 1.9 * STEP) == (1, 2)


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_small_graph_known_path(algo):
    #   A --1000-- B --1000-- D
    #    \                   /
    #     ------ C ---------      A→C→D dài hơn tổng A→B→D
    coords = {"A": (LAT0, LNG0), "B": (LAT0, LNG0 + STEP), "C": (LAT0 - STEP, LNG0 + STEP), "D": (LAT0, LNG0 + 2 * STEP)}
    G = make_graph([("A", "B", 1000), ("B", "D", 1000), ("A", "C", 1500), ("C", "D", 1500)], coords)

    result = algo(G, "A", "D")

    assert result["path"] == ["A", "B", "D"]
    assert result["distance_m"] == 2000
    assert result["visited_count"] == len(result["visited_nodes"])
    assert result["visited_nodes"][0] == "A"
    assert result["visited_nodes"][-1] == "D"
    assert result["runtime_ms"] >= 0


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_respects_one_way(algo):
    coords = {"A": (LAT0, LNG0), "B": (LAT0, LNG0 + STEP)}
    G = make_graph([("A", "B")], coords)

    assert algo(G, "A", "B")["path"] == ["A", "B"]
    with pytest.raises(NoPathError):
        algo(G, "B", "A")


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_no_path_between_components(algo):
    coords = {"A": (LAT0, LNG0), "B": (LAT0, LNG0 + STEP), "C": (LAT0 + STEP, LNG0)}
    G = make_graph([("A", "B"), ("B", "A")], coords)

    with pytest.raises(NoPathError):
        algo(G, "A", "C")


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_start_equals_goal(algo):
    G = make_graph([], {"A": (LAT0, LNG0)})
    result = algo(G, "A", "A")
    assert result["path"] == ["A"]
    assert result["distance_m"] == 0


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_parallel_edges_use_shortest(algo):
    coords = {"A": (LAT0, LNG0), "B": (LAT0, LNG0 + STEP)}
    G = make_graph([("A", "B", 500), ("A", "B", 200), ("A", "B", 900)], coords, multi=True)
    assert algo(G, "A", "B")["distance_m"] == 200


@pytest.mark.parametrize("seed", range(5))
def test_matches_networkx_on_grid(seed):
    G = make_grid(15, seed)
    rng = random.Random(seed)
    nodes = list(G.nodes)
    for _ in range(20):
        start, goal = rng.choice(nodes), rng.choice(nodes)
        expected = nx.shortest_path_length(G, start, goal, weight="length")

        d = dijkstra(G, start, goal)
        a = astar(G, start, goal)

        assert d["distance_m"] == pytest.approx(expected)
        assert a["distance_m"] == pytest.approx(expected)
        # A* không bao giờ duyệt nhiều node hơn Dijkstra khi heuristic nhất quán
        assert a["visited_count"] <= d["visited_count"]


@pytest.mark.skipif(not settings.graph_cache_file.exists(), reason="Chưa có file bản đồ cache")
def test_real_map_matches_networkx():
    import osmnx as ox

    G = ox.load_graphml(settings.graph_cache_file)
    rng = random.Random(42)
    nodes = list(G.nodes)
    checked = 0
    while checked < 20:
        start, goal = rng.choice(nodes), rng.choice(nodes)
        if not nx.has_path(G, start, goal):
            continue
        expected = nx.shortest_path_length(G, start, goal, weight="length")
        assert dijkstra(G, start, goal)["distance_m"] == pytest.approx(expected)
        assert astar(G, start, goal)["distance_m"] == pytest.approx(expected)
        checked += 1
