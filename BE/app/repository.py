# Đọc/ghi database: bản đồ, lịch sử tìm đường, kết quả benchmark
import networkx as nx
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.models import BenchmarkResult, BenchmarkRun, Edge, Map, Node, RouteQuery


def _text(value, limit: int) -> str | None:
    """OSMnx gộp nhiều đoạn đường thành một cạnh nên name, highway... có thể là list."""
    if value is None:
        return None
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)
    return str(value)[:limit]


def load_graph(session: Session, map_name: str) -> tuple[int, nx.MultiDiGraph] | None:
    """Dựng lại đồ thị OSMnx từ bảng nodes, edges. Chưa có bản đồ thì trả về None."""
    map_id = session.scalar(select(Map.id).where(Map.name == map_name))
    if map_id is None:
        return None

    G = nx.MultiDiGraph(crs="epsg:4326")
    for osm_id, lat, lng, street_count in session.execute(
        select(Node.osm_id, Node.lat, Node.lng, Node.street_count).where(Node.map_id == map_id)
    ):
        G.add_node(osm_id, y=lat, x=lng, street_count=street_count)
    for e in session.scalars(select(Edge).where(Edge.map_id == map_id)):
        G.add_edge(
            e.u,
            e.v,
            key=e.edge_key,
            length=e.length,
            name=e.name,
            highway=e.highway,
            oneway=e.oneway,
            maxspeed=e.maxspeed,
        )
    return map_id, G


def save_graph(session: Session, map_name: str, G: nx.MultiDiGraph) -> int:
    """Lưu toàn bộ node, cạnh của đồ thị. Trả về id bản đồ."""
    m = Map(name=map_name, node_count=G.number_of_nodes(), edge_count=G.number_of_edges())
    session.add(m)
    session.flush()

    session.execute(
        insert(Node),
        [
            {"map_id": m.id, "osm_id": n, "lat": d["y"], "lng": d["x"], "street_count": d.get("street_count")}
            for n, d in G.nodes(data=True)
        ],
    )
    session.execute(
        insert(Edge),
        [
            {
                "map_id": m.id,
                "u": u,
                "v": v,
                "edge_key": k,
                "length": float(d["length"]),
                "name": _text(d.get("name"), 255),
                "highway": _text(d.get("highway"), 64),
                "oneway": bool(d.get("oneway", False)),
                "maxspeed": _text(d.get("maxspeed"), 64),
            }
            for u, v, k, d in G.edges(keys=True, data=True)
        ],
    )
    session.commit()
    return m.id


def save_route_query(session: Session, **fields) -> None:
    session.add(RouteQuery(**fields))
    session.commit()


def recent_route_queries(session: Session, map_id: int, limit: int) -> list[RouteQuery]:
    return list(
        session.scalars(
            select(RouteQuery).where(RouteQuery.map_id == map_id).order_by(RouteQuery.id.desc()).limit(limit)
        )
    )


def save_benchmark(session: Session, map_id: int, seed: int, pair_count: int, rows: list[dict]) -> int:
    run = BenchmarkRun(map_id=map_id, seed=seed, pair_count=pair_count)
    session.add(run)
    session.flush()
    session.execute(insert(BenchmarkResult), [{"run_id": run.id, **row} for row in rows])
    session.commit()
    return run.id
