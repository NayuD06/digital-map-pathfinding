# Dựng bản đồ từ file .osm.pbf (Geofabrik) thay cho Overpass, dùng khi Overpass quá tải.
#
# Trong thư mục BE/:
#   pip install osmium
#   (tải https://download.geofabrik.de/asia/vietnam-latest.osm.pbf, khoảng 330 MB)
#   python -m scripts.graph_from_pbf duong/dan/vietnam-latest.osm.pbf
#
# Lấy theo PLACE_NAME và GRAPH_BUFFER_KM trong .env, ghi vào file cache của bản đồ
# (data/<tên bản đồ>.graphml); lần khởi động BE sau sẽ đọc file này như khi tải từ Overpass.
import logging
import re
import sys
import tempfile
import time
from pathlib import Path
from xml.sax.saxutils import quoteattr

import networkx as nx
import numpy as np
import osmium
import osmnx as ox
import shapely
from osmnx._overpass import _get_network_filter

from app.config import settings
from app.graph_loader import boundary_polygon

logger = logging.getLogger(__name__)

# Dùng đúng bộ lọc "drive" của OSMnx, ví dụ ["highway"!~"footway|path|..."]["service"!~"parking|..."]
NETWORK_TYPE = "drive"
EXCLUDE = re.findall(r'\["(\w+)"!~"([^"]+)"\]', _get_network_filter(NETWORK_TYPE))
USEFUL_TAGS = set(ox.settings.useful_tags_way) | {"highway"}


def is_drivable(tags) -> bool:
    # Giống Overpass: "!~" đạt khi không có tag hoặc giá trị không khớp regex (không neo đầu/cuối)
    return "highway" in tags and not any(k in tags and re.search(p, tags[k]) for k, p in EXCLUDE)


def read_ways(pbf: Path, polygon) -> tuple[dict, list]:
    """Lấy các đường cho ô tô có ít nhất một node trong ranh giới, cùng tọa độ các node của chúng."""
    west, south, east, north = polygon.bounds
    nodes, ways = {}, []
    processor = (
        osmium.FileProcessor(pbf, osmium.osm.NODE | osmium.osm.WAY)
        .with_locations()
        .with_filter(osmium.filter.EntityFilter(osmium.osm.WAY))
        .with_filter(osmium.filter.KeyFilter("highway"))
    )
    for way in processor:
        if not is_drivable(way.tags):
            continue
        points = [(n.ref, n.lat, n.lon) for n in way.nodes if n.location.valid()]
        if not any(south <= lat <= north and west <= lon <= east for _, lat, lon in points):
            continue
        nodes.update((ref, (lat, lon)) for ref, lat, lon in points)
        # OSMnx chỉ giữ các tag trong useful_tags_way, bỏ bớt từ đây cho nhẹ bộ nhớ
        tags = {k: way.tags[k] for k in USEFUL_TAGS if k in way.tags}
        ways.append((way.id, [ref for ref, _, _ in points], tags))

    # Khung bao của TP.HCM mới chứa cả nhiều tỉnh lân cận: lọc lại theo đúng ranh giới
    ids = np.fromiter(nodes, dtype=np.int64, count=len(nodes))
    lat_lng = np.array(list(nodes.values()))
    shapely.prepare(polygon)
    inside = set(ids[shapely.contains_xy(polygon, lat_lng[:, 1], lat_lng[:, 0])].tolist())
    ways = [way for way in ways if any(ref in inside for ref in way[1])]
    nodes = {ref: nodes[ref] for _, refs, _ in ways for ref in refs}
    return nodes, ways


def write_osm_xml(path: Path, nodes: dict, ways: list) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<osm version="0.6">\n')
        for ref, (lat, lon) in nodes.items():
            f.write(f'<node id="{ref}" lat="{lat:.7f}" lon="{lon:.7f}"/>\n')
        for way_id, refs, tags in ways:
            f.write(f'<way id="{way_id}">')
            f.writelines(f'<nd ref="{ref}"/>' for ref in refs)
            f.writelines(f"<tag k={quoteattr(k)} v={quoteattr(v)}/>" for k, v in tags.items())
            f.write("</way>\n")
        f.write("</osm>\n")


def main(pbf: Path) -> None:
    started = time.time()
    polygon = boundary_polygon()
    logger.info("Ranh giới %s: khung bao %s", settings.map_name, polygon.bounds)

    nodes, ways = read_ways(pbf, polygon)
    logger.info("Đọc %s: %d đường, %d node (%.0f giây)", pbf.name, len(ways), len(nodes), time.time() - started)

    with tempfile.TemporaryDirectory() as tmp:
        xml_path = Path(tmp) / "network.osm"
        write_osm_xml(xml_path, nodes, ways)
        del nodes, ways
        G_all = ox.graph_from_xml(xml_path, retain_all=True, simplify=True)

    # Như graph_from_place: rút gọn trước, cắt theo ranh giới sau, đếm số đường ở mỗi nút
    # trên đồ thị chưa cắt để nút sát ranh giới vẫn đếm đủ
    G = ox.truncate.truncate_graph_polygon(G_all, polygon)
    nx.set_node_attributes(G, ox.stats.count_streets_per_node(G_all, nodes=G.nodes), "street_count")
    del G_all

    path = settings.graph_cache_file
    path.parent.mkdir(parents=True, exist_ok=True)
    ox.save_graphml(G, path)
    logger.info(
        "Đã lưu %s: %d node, %d cạnh (%.0f giây)", path, len(G), G.number_of_edges(), time.time() - started
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) != 2:
        sys.exit("Cách dùng: python -m scripts.graph_from_pbf duong/dan/file.osm.pbf")
    main(Path(sys.argv[1]))
