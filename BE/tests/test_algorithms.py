
"""Kiểm thử các thuật toán tìm đường của TV3."""

import random
from itertools import pairwise

import networkx as nx
import pytest

from app.algorithms.astar import astar
from app.algorithms.bidirectional import bidirectional
from app.algorithms.dijkstra import dijkstra
from app.algorithms.utils import (
    NoPathError,
    haversine,
    nearest_node,
    neighbors,
    reconstruct_path,
)
from app.config import settings

ALGOS = [dijkstra, astar, bidirectional]


@pytest.fixture
def small_graph():
    G = nx.MultiDiGraph()

    coords = {
        1: (10.7700, 106.6900),
        2: (10.7702, 106.6902),
        3: (10.7698, 106.6902),
        4: (10.7700, 106.6904),
    }

    for node, (lat, lng) in coords.items():
        G.add_node(node, y=lat, x=lng)

    edges = [
        (1, 2, 100.0),
        (2, 4, 100.0),
        (1, 3, 150.0),
        (3, 4, 150.0),
    ]

    for u, v, length in edges:
        G.add_edge(u, v, length=length)

    return G


@pytest.fixture
def grid_graph():
    """Tạo đồ thị lưới với trọng số địa lý hợp lệ."""
    G = nx.MultiDiGraph()

    rows = 12
    cols = 12

    for r in range(rows):
        for c in range(cols):
            node = r * cols + c

            G.add_node(
                node,
                y=10.7700 + r * 0.0001,
                x=106.6900 + c * 0.0001,
            )

    for r in range(rows):
        for c in range(cols):
            u = r * cols + c

            for dr, dc in [(0, 1), (1, 0)]:
                nr = r + dr
                nc = c + dc

                if nr >= rows or nc >= cols:
                    continue

                v = nr * cols + nc

                length = haversine(
                    G.nodes[u]["y"],
                    G.nodes[u]["x"],
                    G.nodes[v]["y"],
                    G.nodes[v]["x"],
                ) * 1.2

                G.add_edge(u, v, length=length)
                G.add_edge(v, u, length=length)

    return G


def test_haversine_known_distance():
    result = haversine(10, 106, 11, 106)

    assert result == pytest.approx(
        111_195,
        rel=1e-3,
    )


def test_haversine_same_point():
    assert haversine(10, 106, 10, 106) == 0.0


def test_haversine_symmetry():
    a = haversine(10, 106, 11, 107)
    b = haversine(11, 107, 10, 106)

    assert a == pytest.approx(b)


def test_haversine_antipodal():
    result = haversine(0, 0, 0, 180)

    assert result == pytest.approx(
        20_015_087,
        rel=1e-5,
    )


def test_reconstruct_path():
    parent = {
        2: 1,
        3: 2,
        4: 3,
    }

    assert reconstruct_path(
        parent, 1, 4
    ) == [1, 2, 3, 4]


def test_reconstruct_same_node():
    assert reconstruct_path({}, 1, 1) == [1]


def test_nearest_node(small_graph):
    result = nearest_node(
        small_graph,
        10.7700,
        106.6900,
    )

    assert result == 1


def test_neighbors_parallel_edges(small_graph):
    small_graph.add_edge(
        1, 2, length=80.0
    )

    result = dict(neighbors(small_graph, 1))

    assert result[2] == 80.0
    assert result[3] == 150.0


def test_neighbors_simple_graph():
    G = nx.DiGraph()

    G.add_edge(1, 2, length=100.0)

    assert dict(neighbors(G, 1)) == {
        2: 100.0,
    }


@pytest.mark.parametrize("algo", ALGOS)
def test_small_graph(algo, small_graph):
    result = algo(small_graph, 1, 4)

    assert result["path"] == [1, 2, 4]
    assert result["distance_m"] == 200.0


@pytest.mark.parametrize("algo", ALGOS)
def test_parallel_edges(algo, small_graph):
    small_graph.add_edge(
        1, 2, length=80.0
    )

    result = algo(small_graph, 1, 4)

    assert result["path"] == [1, 2, 4]
    assert result["distance_m"] == 180.0


@pytest.mark.parametrize("algo", ALGOS)
def test_same_start_goal(algo, small_graph):
    result = algo(small_graph, 1, 1)

    assert result["path"] == [1]
    assert result["distance_m"] == 0.0
    assert result["visited_count"] == 1


@pytest.mark.parametrize("algo", ALGOS)
def test_no_path(algo, small_graph):
    with pytest.raises(NoPathError):
        algo(small_graph, 4, 1)


@pytest.mark.parametrize("algo", ALGOS)
def test_disconnected_graph(algo, small_graph):
    small_graph.add_node(
        99,
        y=10.7800,
        x=106.7000,
    )

    with pytest.raises(NoPathError):
        algo(small_graph, 1, 99)


@pytest.mark.parametrize("algo", ALGOS)
def test_invalid_node(algo, small_graph):
    with pytest.raises(NoPathError):
        algo(small_graph, 1, 999)


@pytest.mark.parametrize("algo", ALGOS)
def test_result_structure(algo, small_graph):
    result = algo(small_graph, 1, 4)

    assert set(result.keys()) == {
        "path",
        "distance_m",
        "visited_count",
        "visited_nodes",
        "runtime_ms",
    }

    assert isinstance(result["path"], list)
    assert isinstance(result["distance_m"], float)
    assert isinstance(result["visited_count"], int)
    assert isinstance(result["visited_nodes"], list)
    assert isinstance(result["runtime_ms"], float)

    assert result["runtime_ms"] >= 0

    assert result["visited_count"] == len(
        result["visited_nodes"]
    )

    assert len(set(result["visited_nodes"])) == len(
        result["visited_nodes"]
    )


@pytest.mark.parametrize("algo", ALGOS)
def test_matches_networkx(algo, grid_graph):
    rng = random.Random(42)
    nodes = list(grid_graph.nodes)

    for _ in range(30):
        start, goal = rng.sample(nodes, 2)

        result = algo(
            grid_graph,
            start,
            goal,
        )

        expected = nx.shortest_path_length(
            grid_graph,
            start,
            goal,
            weight="length",
        )

        assert result["distance_m"] == pytest.approx(
            expected
        )

        path = result["path"]

        assert path[0] == start
        assert path[-1] == goal

        actual_length = sum(
            min(
                edge["length"]
                for edge in grid_graph[u][v].values()
            )
            for u, v in pairwise(path)
        )

        assert actual_length == pytest.approx(
            expected
        )


def test_astar_visited_nodes(grid_graph):
    d = dijkstra(grid_graph, 0, 143)
    a = astar(grid_graph, 0, 143)

    assert d["distance_m"] == pytest.approx(
        a["distance_m"]
    )

    assert a["visited_count"] <= d["visited_count"]


def test_bidirectional_not_first_meeting():
    """Không được dừng ngay khi hai hướng gặp nhau."""
    G = nx.MultiDiGraph()

    G.add_edge("S", "A", length=1.0)
    G.add_edge("A", "T", length=100.0)
    G.add_edge("S", "B", length=50.0)
    G.add_edge("B", "T", length=2.0)

    result = bidirectional(G, "S", "T")

    assert result["distance_m"] == 52.0
    assert result["path"] == ["S", "B", "T"]


@pytest.mark.skipif(
    not settings.graph_cache_file.exists(),
    reason="Chưa có cache bản đồ thật",
)
def test_real_map():
    import osmnx as ox

    # Đọc trực tiếp cache, không tải lại từ Internet.
    G = ox.io.load_graphml(
        settings.graph_cache_file
    )

    G = ox.truncate.largest_component(
        G,
        strongly=True,
    )

    nodes = list(G.nodes)
    rng = random.Random(42)

    for _ in range(20):
        start, goal = rng.sample(nodes, 2)

        expected = nx.shortest_path_length(
            G,
            start,
            goal,
            weight="length",
        )

        for algo in ALGOS:
            result = algo(G, start, goal)

            assert result["distance_m"] == pytest.approx(
                expected
            )

            path = result["path"]

            assert path[0] == start
            assert path[-1] == goal

            actual_length = sum(
                min(
                    edge["length"]
                    for edge in G[u][v].values()
                )
                for u, v in pairwise(path)
            )

            assert actual_length == pytest.approx(
                expected
            )
