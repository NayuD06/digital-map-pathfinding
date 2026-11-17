# Hướng dẫn thực hiện cho từng thành viên

Tài liệu này hướng dẫn **TV2, TV3, TV4, TV5** làm phần việc của mình trong [04-phan-cong.md](04-phan-cong.md): sửa file nào, làm theo thứ tự nào, gợi ý cách code, cách tự kiểm tra và phần báo cáo cần viết. Mã công việc (ví dụ `2.3`) tham chiếu tới [03-chuc-nang-can-lam.md](03-chuc-nang-can-lam.md). Định dạng dữ liệu giữa FE và BE xem ở [05-dinh-dang-api.md](05-dinh-dang-api.md). Dàn ý chi tiết phần báo cáo và thuyết trình của từng người xem ở [07-noi-dung-tung-nguoi.md](07-noi-dung-tung-nguoi.md).

> Các đoạn code mẫu bên dưới đã được chạy thử trên bản đồ Quận 1 thật: Dijkstra và A\* cho cùng độ dài đường đi, khớp với `networkx.shortest_path_length`, FE vẽ được đường đi và biểu đồ khi nối với BE. Đây là **gợi ý**, mỗi người cần đọc hiểu và tự viết lại theo cách của mình để trả lời được khi bảo vệ.

**Mục lục**

- [0. Việc chung cho mọi người](#0-việc-chung-cho-mọi-người)
- [1. TV2 – BE: Dữ liệu bản đồ](#1-tv2--be-dữ-liệu-bản-đồ)
- [2. TV3 – BE: Thuật toán](#2-tv3--be-thuật-toán)
- [3. TV4 – FE: Bản đồ](#3-tv4--fe-bản-đồ)
- [4. TV5 – FE: Giao diện và đánh giá](#4-tv5--fe-giao-diện-và-đánh-giá)
- [5. Việc còn lại của nhóm trưởng (TV1)](#5-việc-còn-lại-của-nhóm-trưởng-tv1)
- [6. Lỗi thường gặp](#6-lỗi-thường-gặp)
- [7. Thế nào là "xong việc"](#7-thế-nào-là-xong-việc)

---

## 0. Việc chung cho mọi người

### 0.1 Tình trạng hiện tại

Phần của nhóm trưởng (TV1) đã xong, nằm ở nhánh `feature/nhom-truong`:

| Đã có | File |
|---|---|
| Đọc cấu hình `.env`, khởi tạo FastAPI, CORS, `GET /health` | `BE/app/config.py`, `BE/app/main.py` |
| Định dạng API đã chốt | `BE/app/schemas.py`, [05-dinh-dang-api.md](05-dinh-dang-api.md) |
| `GET /api/graph/info`, `GET /api/route`, lỗi 400/404/503 | `BE/app/api/routes.py` |
| Khung hàm cho TV2, TV3 (đúng tên, tham số, docstring; bên trong là `raise NotImplementedError`) | `graph_loader.py`, `algorithms/*.py` |
| Test API | `BE/tests/test_api.py` |
| Hàm gọi API bên FE và dữ liệu giả để làm FE khi chưa có BE | `FE/src/api/client.js`, `FE/src/api/mock.js` |

**Mọi người tạo nhánh từ `main` sau khi nhánh `feature/nhom-truong` đã được merge.** Cách kiểm tra: trên `main` đã có file `docs/05-dinh-dang-api.md`. Nếu chưa có thì nhắn nhóm trưởng.

Việc của mỗi người là thay các `raise NotImplementedError(...)` bằng code thật và làm các file còn trống. **Không đổi tên hàm, tham số và kiểu trả về đã chốt**, vì `main.py` và `routes.py` đang gọi đúng các tên đó. Muốn đổi thì báo nhóm trưởng để sửa cùng lúc cả `schemas.py`, `client.js`, `mock.js` và [05-dinh-dang-api.md](05-dinh-dang-api.md).

### 0.2 Cài đặt (làm một lần)

Cần cài: **Python 3.12**, **Node.js 20**, **Git**.

**Backend** (terminal 1, lệnh cho Windows):

```bash
cd BE
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install ruff
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

> macOS/Linux: `source .venv/bin/activate` và `cp .env.example .env`.

Mở http://localhost:8000/health phải thấy `{"status":"ok"}`, http://localhost:8000/docs là trang thử API. Khi TV2 chưa làm xong `graph_loader.py`, các API bản đồ trả **503 "Server chưa nạp bản đồ"**, đây là bình thường.

**Frontend** (terminal 2):

```bash
cd FE
npm install
copy .env.example .env
npm run dev
```

Mở http://localhost:5173. Muốn làm FE khi BE chưa chạy được thì sửa `FE/.env` thành `VITE_USE_MOCK=true` rồi chạy lại `npm run dev` (Vite chỉ đọc `.env` lúc khởi động).

### 0.3 Quy trình Git

Tóm tắt mục 5 của [04-phan-cong.md](04-phan-cong.md):

```bash
git checkout main
git pull origin main
git checkout -b feature/ten-chuc-nang
# ... code, chạy kiểm tra ở mục 0.4 ...
git add <các file đã sửa>
git commit -m "Thêm thuật toán A* với heuristic Haversine"
git push -u origin feature/ten-chuc-nang
```

Lên GitHub tạo Pull Request vào `main`, chờ CI xanh và nhóm trưởng review. **Không push thẳng lên `main`.** Mỗi PR chỉ nên làm một việc, càng nhỏ càng dễ review.

Gợi ý tên nhánh:

| TV | Nhánh code | Nhánh báo cáo |
|---|---|---|
| TV2 | `feature/graph-loader`, `feature/traffic` | `docs/bao-cao-ban-do` |
| TV3 | `feature/dijkstra-astar`, `feature/bidirectional` | `docs/bao-cao-thuat-toan` |
| TV4 | `feature/app-layout`, `feature/map-view` | `docs/bao-cao-he-thong-thuc-te` |
| TV5 | `feature/control-stats`, `feature/compare-api`, `feature/benchmark` | `docs/bao-cao-thuc-nghiem` |

Phần báo cáo viết bằng Markdown trong thư mục `docs/bao-cao/`, đặt tên theo mã mục giống file nhóm trưởng đã có (`1.14-ket-luan.md`), ví dụ `docs/bao-cao/1.7-dijkstra.md`. Nhóm trưởng sẽ ghép thành báo cáo cuối.

### 0.4 Chạy kiểm tra giống CI trước khi push

```bash
cd BE
ruff check .          # lỗi đơn giản thì sửa tự động: ruff check . --fix
pytest
cd ../FE
npm run build
```

CI không có file bản đồ, nên **test không được tải bản đồ từ mạng**. Test cần bản đồ thật phải tự bỏ qua khi không có file (xem ví dụ `skipif` ở mục 2, bước 6).

### 0.5 Không commit những file này

`.env`, `BE/data/*.graphml`, `BE/data/osmnx_cache/`, `node_modules/`, `dist/`. Đã có trong `.gitignore`. Trước khi commit, chạy `git status` xem lại danh sách file. Lỡ commit file lớn thì báo nhóm trưởng trước khi merge.

### 0.6 Ai chờ ai

| Người | Bắt đầu được ngay? | Ghi chú |
|---|---|---|
| TV2 | Có | |
| TV3 | Có | Viết và test trên đồ thị nhỏ tự tạo, không cần chờ TV2 |
| TV4 | Có | Dùng `VITE_USE_MOCK=true` |
| TV5 | Có | FE dùng mock; `/api/compare` test được bằng thuật toán giả; `/api/benchmark` cần TV2, TV3 xong mới chạy thật |

**Thỏa thuận giữa TV4 và TV5.** TV4 làm `App.jsx` (giữ trạng thái), TV5 làm các component hiển thị. Hai bạn thống nhất props như bảng dưới để làm song song:

| Component (người làm) | Props nhận từ `App.jsx` |
|---|---|
| `MapView` (TV4) | `graphInfo`, `start`, `end`, `results`, `showVisited`, `onMapClick(latlng)`, `onStartMove(latlng)`, `onEndMove(latlng)` |
| `ControlPanel` (TV5) | `algo`, `onAlgoChange(algo)`, `canRun`, `loading`, `error`, `showVisited`, `onShowVisitedChange(bool)`, `onFind()`, `onCompare()`, `onClear()` |
| `StatsPanel` (TV5) | `results` |
| `CompareChart` (TV5) | `results` (chỉ hiện khi có 2 kết quả) |

- `start`, `end` có dạng `{ lat, lng }` (hoặc `null` khi chưa chọn).
- `results` **luôn là mảng** các kết quả đúng định dạng `GET /api/route`: bấm Tìm đường thì có 1 phần tử, bấm So sánh thì là `response.results` (2 phần tử).
- Màu và tên hiển thị của thuật toán để chung trong `FE/src/constants.js` (TV4 tạo trước, xem mục 3).

---

## 1. TV2 – BE: Dữ liệu bản đồ

**Phụ trách:** `BE/app/graph_loader.py` (`load_graph`, `graph_info`), hàm `nearest_node` trong `BE/app/algorithms/utils.py`, mở rộng `2.7` (trọng số theo thời gian, kẹt xe). Báo cáo `1.1`–`1.4`.

**Kết quả cần đạt:** khởi động server lần 2 đọc bản đồ từ file cache, không tải lại; `GET /api/graph/info` trả đúng số node, số cạnh, khung bao, tâm bản đồ.

### Bước 1. Tải thử bản đồ để hiểu dữ liệu

Chạy thử trong Python (đã kích hoạt `.venv`) trước khi viết code:

```python
import osmnx as ox

G = ox.graph_from_place("District 1, Ho Chi Minh City, Vietnam", network_type="drive")
print(type(G), len(G.nodes), len(G.edges))
u, v, data = next(iter(G.edges(data=True)))
print(G.nodes[u])        # {'y': 10.77..., 'x': 106.69..., ...}  y = vĩ độ (lat), x = kinh độ (lng)
print(data["length"])    # độ dài đoạn đường, đơn vị mét
```

Những điều cần nắm (cũng là nội dung báo cáo `1.2`):

- `G` là `networkx.MultiDiGraph`: **có hướng** (đường một chiều chỉ có cạnh một chiều) và giữa 2 node **có thể có nhiều cạnh song song**.
- Node là giao lộ hoặc điểm cuối đường, có `y` (lat) và `x` (lng). Cạnh là đoạn đường, có `length` (mét), `highway`, `oneway`, `name`...
- `network_type="drive"`: chỉ lấy đường cho ô tô.

### Bước 2. Viết `load_graph(place_name, cache_file)`

`main.py` gọi hàm này một lần khi khởi động. `cache_file` là đường dẫn tuyệt đối tới file cache (mặc định `BE/data/graph.graphml`, lấy từ `GRAPH_CACHE_PATH` trong `.env`).

```python
import logging
from pathlib import Path

import osmnx as ox

logger = logging.getLogger(__name__)


def load_graph(place_name: str, cache_file: Path):
    # OSMnx mặc định lưu cache HTTP vào ./cache ở nơi chạy lệnh; gom về data/osmnx_cache (đã có trong .gitignore)
    ox.settings.cache_folder = cache_file.parent / "osmnx_cache"

    if cache_file.exists():
        logger.info("Đọc bản đồ từ cache %s", cache_file)
        G = ox.load_graphml(cache_file)
    else:
        logger.info("Tải bản đồ %s từ OpenStreetMap...", place_name)
        G = ox.graph_from_place(place_name, network_type="drive")
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        ox.save_graphml(G, cache_file)

    # Giữ thành phần liên thông mạnh lớn nhất: bỏ các đoạn đường cụt ở ranh giới quận
    # để 2 điểm bất kỳ trên bản đồ luôn có đường đi
    return ox.truncate.largest_component(G, strongly=True)
```

Giải thích:

- **Cache:** lần đầu tải từ OpenStreetMap mất vài chục giây đến vài phút. Lần sau đọc từ `.graphml` chỉ mất 1–2 giây.
- **`largest_component(strongly=True)`:** đường bị cắt ở ranh giới quận để lại những node chỉ đi vào hoặc chỉ đi ra. Nếu giữ lại, người dùng click vào đó sẽ bị lỗi 404 "không có đường". Bỏ đi thì giữa 2 node bất kỳ luôn có đường.
- Máy chủ OpenStreetMap (Overpass) đôi khi quá tải, trả lỗi 429/504. Cứ chạy lại, phần đã tải nằm trong `osmnx_cache` nên không phải tải lại từ đầu.
- `main.py` chỉ bỏ qua `NotImplementedError`. Nếu `load_graph` ném lỗi khác (ví dụ mất mạng lúc tải lần đầu) thì server không khởi động và lỗi in ra terminal, đọc lỗi để sửa.

### Bước 3. Viết `graph_info(G, place_name)`

Trả về đúng định dạng `GraphInfo` trong `schemas.py`. `bbox` là `[south, west, north, east]`, `center` là `[lat, lng]`.

```python
def graph_info(G, place_name: str) -> dict:
    lats = [data["y"] for _, data in G.nodes(data=True)]
    lngs = [data["x"] for _, data in G.nodes(data=True)]
    south, north, west, east = min(lats), max(lats), min(lngs), max(lngs)
    return {
        "place_name": place_name,
        "node_count": G.number_of_nodes(),
        "edge_count": G.number_of_edges(),
        "bbox": [south, west, north, east],
        "center": [(south + north) / 2, (west + east) / 2],
    }
```

`routes.py` dùng `bbox` này để trả lỗi 400 khi người dùng chọn điểm ngoài vùng bản đồ, và FE dùng nó để vẽ khung đứt nét.

### Bước 4. Viết `nearest_node(G, lat, lng)` trong `algorithms/utils.py`

Người dùng click một điểm bất kỳ, phải bắt về node gần nhất trên đồ thị. Cách đơn giản, đủ nhanh cho một quận (vài nghìn node, chỉ mất vài mili giây):

```python
def nearest_node(G, lat: float, lng: float):
    """Id của node gần tọa độ (lat, lng) nhất. Node có thuộc tính y = lat, x = lng."""
    return min(G.nodes, key=lambda n: haversine(lat, lng, G.nodes[n]["y"], G.nodes[n]["x"]))
```

- `haversine` do TV3 viết trong cùng file. Nếu TV3 chưa xong, tạm dùng `ox.distance.great_circle(lat1, lng1, lat2, lng2)` (nhớ `import osmnx as ox`), sau đổi lại.
- Cách khác là `ox.distance.nearest_nodes(G, X=lng, Y=lat)`, nhưng với đồ thị chưa chiếu (tọa độ độ) hàm này **cần cài thêm `scikit-learn`** (phải thêm vào `requirements.txt`). Nếu dùng cách này thì ghi rõ trong báo cáo.

### Bước 5. Tự kiểm tra

1. Chạy `uvicorn app.main:app --reload --port 8000`. Lần đầu sẽ tải bản đồ, xong thì thấy file `BE/data/graph.graphml`.
2. Tắt rồi chạy lại: server lên ngay, không tải lại.
3. Mở http://localhost:8000/api/graph/info, kiểm tra số node, số cạnh, `bbox` hợp lý (Quận 1 khoảng lat 10.75–10.80, lng 106.68–106.72).
4. Lúc này `/api/route` vẫn lỗi 500 vì thuật toán của TV3 chưa xong, đúng như dự kiến.

Viết test cho phần mình, trao đổi với TV3 (người giữ thư mục `tests/`) để không trùng. Ví dụ `tests/test_graph_loader.py`, dùng đồ thị nhỏ lưu ra file tạm nên **không cần mạng**:

```python
import networkx as nx
import osmnx as ox
import pytest

from app.graph_loader import graph_info, load_graph


def small_graph():
    G = nx.MultiDiGraph(crs="epsg:4326")
    G.add_node(1, y=10.770, x=106.690)
    G.add_node(2, y=10.780, x=106.700)
    G.add_edge(1, 2, length=150.0)
    G.add_edge(2, 1, length=150.0)
    return G


def test_load_graph_reads_cache(tmp_path):
    path = tmp_path / "graph.graphml"
    ox.save_graphml(small_graph(), path)
    G = load_graph("Test", path)  # có file rồi nên không tải từ mạng
    assert set(G.nodes) == {1, 2}
    assert G.number_of_edges() == 2


def test_graph_info():
    info = graph_info(small_graph(), "Test")
    assert info["node_count"] == 2
    assert info["bbox"] == [10.770, 106.690, 10.780, 106.700]
    assert info["center"] == pytest.approx([10.775, 106.695])  # số thực nên so sánh gần đúng
```

### Bước 6 (mở rộng, P3). Trọng số theo thời gian và giả lập kẹt xe

**Trọng số theo thời gian:**

```python
G = ox.routing.add_edge_speeds(G)        # thêm speed_kph cho mỗi cạnh (theo maxspeed hoặc loại đường)
G = ox.routing.add_edge_travel_times(G)  # thêm travel_time (giây)
```

Thuật toán của TV3 đang dùng `length`. Muốn tìm đường nhanh nhất thì cần thêm tham số chọn trọng số (ví dụ `weight="length" | "travel_time"`) cho thuật toán và API. Việc này đổi định dạng API nên phải bàn với TV1 và TV3 trước.

**Giả lập kẹt xe** (`POST /api/traffic`, `DELETE /api/traffic`):

- `POST` nhận `{lat, lng, radius_m, factor}`: với các cạnh có trung điểm nằm trong bán kính, lưu độ dài gốc vào `length_orig` (nếu chưa có) rồi đặt `length = length_orig * factor`.
- `DELETE` trả mọi cạnh có `length_orig` về độ dài gốc.
- Cần thêm schema vào `schemas.py`, hàm vào `client.js` và mục mới vào [05-dinh-dang-api.md](05-dinh-dang-api.md): làm cùng TV1. Phần chọn đoạn kẹt xe trên bản đồ (`3.6`) làm cùng TV4.
- Kịch bản demo: chạy A\* giữa 2 điểm, đánh dấu kẹt xe một đoạn trên tuyến, chạy lại thấy tuyến đổi hướng.

### Báo cáo TV2 (`docs/bao-cao/1.1-1.4-ban-do-so.md`)

| Mục | Nội dung gợi ý |
|---|---|
| `1.1` Bản đồ số, vai trò trong ITS | Bản đồ số là gì, khác bản đồ giấy ở đâu (dữ liệu có cấu trúc, truy vấn được, cập nhật được). Vai trò trong ITS: dẫn đường, quản lý và điều phối giao thông, gọi xe, giao hàng, xe tự hành (bản đồ độ chính xác cao). |
| `1.2` Mô hình dữ liệu | Mô hình của OSM: node, way, relation, tag (`highway`, `oneway`, `maxspeed`, `lanes`, `name`). OSMnx chuyển thành đồ thị: node là giao lộ, cạnh là đoạn đường, `length` là trọng số. Có thể đưa số node/cạnh Quận 1 lấy từ `/api/graph/info`. |
| `1.3` So sánh nguồn dữ liệu | Bảng so sánh OpenStreetMap, Google Maps, HERE, Mapbox, VietMap theo: giấy phép, chi phí, độ phủ ở Việt Nam, có dữ liệu giao thông thời gian thực không, có API tìm đường không. Kết luận vì sao đề tài chọn OSM (mở, miễn phí, tải được cả mạng đường). |
| `1.4` Hệ tọa độ, tile map | WGS84 (EPSG:4326) dùng lat/lng, Web Mercator (EPSG:3857) dùng để vẽ tile. Tile raster theo `z/x/y`, mỗi ô 256×256 px; vector tile. Leaflet trong FE dùng tile của OSM. Vì sao tính khoảng cách bằng Haversine chứ không dùng Pytago trên lat/lng. |

Tài liệu tham khảo: OSM Wiki (Map features, Elements), tài liệu OSMnx, bài báo *Boeing G. (2017), OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks*.

---

## 2. TV3 – BE: Thuật toán

**Phụ trách:** `haversine`, `reconstruct_path` trong `BE/app/algorithms/utils.py`, `dijkstra.py`, `astar.py`, toàn bộ test trong `BE/tests/` (`2.6`), mở rộng Bidirectional Dijkstra. Báo cáo `1.5`–`1.10`, `1.12`.

**Kết quả cần đạt:** Dijkstra và A\* cho cùng độ dài đường đi, A\* duyệt ít node hơn, kết quả khớp `networkx.shortest_path_length`.

Không cần chờ TV2: viết và test trên đồ thị nhỏ tự tạo bằng `networkx`.

### Cấu trúc kết quả bắt buộc

Cả 2 hàm trả về cùng một dict (đã ghi trong `algorithms/__init__.py`), và **ném `NoPathError` khi không có đường** (API đổi thành lỗi 404):

```python
{
    "path": [node_id, ...],            # từ start tới goal
    "distance_m": float,
    "visited_count": int,
    "visited_nodes": [node_id, ...],   # theo thứ tự duyệt
    "runtime_ms": float,
}
```

### Bước 1. `haversine`

```python
import math

# Bán kính Trái Đất (mét). Lấy nhỏ hơn một chút so với OSMnx (6 371 009 m) để
# heuristic của A* không bao giờ lớn hơn độ dài cạnh mà OSMnx tính.
EARTH_RADIUS_M = 6_371_000


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(a))
```

### Bước 2. `reconstruct_path`

`parent[v] = u` nghĩa là đi tới `v` từ `u`. Lần ngược từ `goal` về `start`:

```python
def reconstruct_path(parent: dict, start, goal) -> list:
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path
```

### Bước 3. Hàm phụ đọc cạnh kề (thêm vào `utils.py`)

Đồ thị OSMnx có thể có **nhiều cạnh song song** giữa 2 node, khi đó lấy cạnh ngắn nhất. Được thêm hàm mới vào `utils.py`, chỉ không đổi tên các hàm đã có.

```python
def neighbors(G, u):
    """Sinh (v, độ dài) cho mỗi cạnh u -> v; nhiều cạnh song song thì lấy cạnh ngắn nhất."""
    for v, edges in G[u].items():
        if G.is_multigraph():
            yield v, min(e["length"] for e in edges.values())
        else:
            yield v, edges["length"]
```

### Bước 4. `dijkstra.py`

```python
import heapq
import math
import time

from app.algorithms.utils import NoPathError, neighbors, reconstruct_path


def dijkstra(G, start, goal) -> dict:
    t0 = time.perf_counter()
    dist = {start: 0.0}
    parent = {}
    visited = set()
    visited_order = []
    heap = [(0.0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:  # bản ghi cũ trong heap, đã có khoảng cách tốt hơn
            continue
        visited.add(u)
        visited_order.append(u)
        if u == goal:
            break
        for v, w in neighbors(G, u):
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))

    if goal not in visited:
        raise NoPathError(f"Không có đường từ {start} tới {goal}")
    return {
        "path": reconstruct_path(parent, start, goal),
        "distance_m": dist[goal],
        "visited_count": len(visited_order),
        "visited_nodes": visited_order,
        "runtime_ms": (time.perf_counter() - t0) * 1000,
    }
```

Những điểm cần hiểu để trả lời khi bảo vệ:

- **Node "đã duyệt"** là node được lấy ra khỏi heap lần đầu. Lúc đó khoảng cách tới nó đã chốt, không thể nhỏ hơn được nữa. `visited_nodes` ghi theo đúng thứ tự này để FE vẽ vùng lan ra.
- `heapq` không hỗ trợ giảm khóa, nên khi tìm được khoảng cách tốt hơn ta **đẩy thêm bản ghi mới**, bản ghi cũ bị bỏ qua khi lấy ra (dòng `if u in visited`).
- **Dừng sớm** khi lấy `goal` ra khỏi heap: vẫn đúng vì khoảng cách tới `goal` đã chốt.
- Đo thời gian bằng `time.perf_counter()`, chỉ đo phần thuật toán.
- Id node của OSM là số nguyên nên so sánh được khi 2 phần tử trong heap cùng khoảng cách. Nếu node là kiểu không so sánh được thì thêm bộ đếm `itertools.count()` vào giữa tuple.

### Bước 5. `astar.py`

Giống Dijkstra, chỉ khác thứ tự ưu tiên trong heap là `f = g + h`, với `g` là độ dài đã đi, `h` là khoảng cách Haversine tới đích.

```python
import heapq
import math
import time

from app.algorithms.utils import NoPathError, haversine, neighbors, reconstruct_path


def astar(G, start, goal) -> dict:
    t0 = time.perf_counter()
    goal_lat, goal_lng = G.nodes[goal]["y"], G.nodes[goal]["x"]

    def h(n):
        return haversine(G.nodes[n]["y"], G.nodes[n]["x"], goal_lat, goal_lng)

    g = {start: 0.0}
    parent = {}
    visited = set()
    visited_order = []
    heap = [(h(start), start)]  # (f = g + h, node)

    while heap:
        _, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        visited_order.append(u)
        if u == goal:
            break
        for v, w in neighbors(G, u):
            ng = g[u] + w
            if ng < g.get(v, math.inf):
                g[v] = ng
                parent[v] = u
                heapq.heappush(heap, (ng + h(v), v))

    if goal not in visited:
        raise NoPathError(f"Không có đường từ {start} tới {goal}")
    return {
        "path": reconstruct_path(parent, start, goal),
        "distance_m": g[goal],
        "visited_count": len(visited_order),
        "visited_nodes": visited_order,
        "runtime_ms": (time.perf_counter() - t0) * 1000,
    }
```

Vì sao A\* vẫn cho đường ngắn nhất: đường thật luôn dài hơn hoặc bằng đường chim bay, nên `h` **không bao giờ ước lượng quá** (chấp nhận được, *admissible*) và thỏa bất đẳng thức tam giác (nhất quán, *consistent*). Nhờ vậy mỗi node chỉ cần duyệt một lần và kết quả giống Dijkstra. Đây cũng là lý do lấy bán kính Trái Đất nhỏ hơn OSMnx một chút ở bước 1.

### Bước 6. Viết test (`tests/test_algorithms.py`)

Danh sách test cần có (`2.6`):

| Test | Ý nghĩa |
|---|---|
| Đồ thị nhỏ biết trước kết quả | Đúng đường đi, đúng độ dài |
| Cạnh song song | Lấy cạnh ngắn nhất |
| `start == goal` | Đường đi `[start]`, độ dài 0 |
| Không có đường (cạnh một chiều) | Ném `NoPathError` |
| Đối chiếu `networkx.shortest_path_length` trên lưới lớn hơn | Độ đúng |
| Bản đồ thật (bỏ qua nếu không có file) | Dijkstra = A\* = networkx, A\* duyệt ít hơn hoặc bằng |
| `haversine`, `reconstruct_path`, `nearest_node` | Hàm tiện ích |

Khung gợi ý:

```python
from pathlib import Path

import networkx as nx
import pytest

from app.algorithms.astar import astar
from app.algorithms.dijkstra import dijkstra
from app.algorithms.utils import NoPathError, haversine

ALGOS = [dijkstra, astar]


@pytest.fixture
def small_graph():
    #   1 --100--> 2 --100--> 4
    #   1 --150--> 3 --150--> 4      đường ngắn nhất 1-2-4 = 200
    G = nx.MultiDiGraph()
    coords = {1: (10.770, 106.690), 2: (10.771, 106.691), 3: (10.769, 106.691), 4: (10.770, 106.692)}
    for n, (lat, lng) in coords.items():
        G.add_node(n, y=lat, x=lng)
    for u, v, length in [(1, 2, 100), (2, 4, 100), (1, 3, 150), (3, 4, 150)]:
        G.add_edge(u, v, length=length)
    return G


def test_haversine_known_distance():
    assert haversine(10, 106, 11, 106) == pytest.approx(111_195, rel=1e-3)  # 1 độ vĩ ~ 111,2 km


@pytest.mark.parametrize("algo", ALGOS)
def test_small_graph(algo, small_graph):
    r = algo(small_graph, 1, 4)
    assert r["path"] == [1, 2, 4]
    assert r["distance_m"] == 200
    assert r["visited_count"] == len(r["visited_nodes"])


@pytest.mark.parametrize("algo", ALGOS)
def test_no_path(algo, small_graph):
    with pytest.raises(NoPathError):
        algo(small_graph, 4, 1)  # cạnh một chiều, không đi ngược được


GRAPH_FILE = Path(__file__).resolve().parent.parent / "data" / "graph.graphml"


@pytest.mark.skipif(not GRAPH_FILE.exists(), reason="chưa có bản đồ thật trong data/ (CI bỏ qua)")
def test_real_map_same_distance():
    import random

    from app.graph_loader import load_graph

    G = load_graph("", GRAPH_FILE)
    rng = random.Random(1)
    for _ in range(20):
        s, t = rng.sample(list(G.nodes), 2)
        d, a = dijkstra(G, s, t), astar(G, s, t)
        expected = nx.shortest_path_length(G, s, t, weight="length")
        assert d["distance_m"] == pytest.approx(expected)
        assert a["distance_m"] == pytest.approx(expected)
        assert a["visited_count"] <= d["visited_count"]
```

Lưu ý: `tests/test_api.py` của nhóm trưởng phải vẫn đạt sau khi bạn sửa.

### Bước 7. Chạy thử trên bản đồ thật

Khi TV2 xong, chạy server rồi gọi thử:

```
http://localhost:8000/api/route?algo=dijkstra&from_lat=10.7735&from_lng=106.7004&to_lat=10.7870&to_lng=106.7050
http://localhost:8000/api/route?algo=astar&from_lat=10.7735&from_lng=106.7004&to_lat=10.7870&to_lng=106.7050
```

Hai kết quả phải có cùng `distance_m`, A\* có `visited_count` nhỏ hơn.

### Bước 8 (mở rộng, P2–P3). Bidirectional Dijkstra (`algorithms/bidirectional.py`)

- Chạy 2 Dijkstra cùng lúc: chiều xuôi từ `start` theo `G[u]`, chiều ngược từ `goal` theo cạnh vào `G.pred[u]`.
- Mỗi lần xét cạnh, nếu node bên kia đã có khoảng cách từ phía còn lại thì cập nhật `best = min(best, d_xuôi + w + d_ngược)` và nhớ node gặp nhau.
- **Điều kiện dừng:** khi `đỉnh_heap_xuôi + đỉnh_heap_ngược >= best`. Dừng ngay khi 2 phía vừa chạm nhau là **sai**, hay bị hỏi khi bảo vệ.
- Đường đi = đường xuôi từ `start` tới node gặp nhau + đường ngược từ node đó tới `goal`. `visited_nodes` gộp node đã duyệt của cả 2 phía theo thứ tự.
- Đăng ký trong `ALGORITHMS` (`algorithms/__init__.py`), thêm `"bidirectional"` vào `Algorithm` trong `schemas.py`, thêm màu trong `FE/src/constants.js`. `/api/compare` của TV5 dùng `get_args(Algorithm)` nên sẽ tự chạy thêm thuật toán mới. Báo TV1, TV4, TV5 khi làm.

### Báo cáo TV3

| Mục | Nội dung gợi ý |
|---|---|
| `1.5` Mô hình hóa mạng giao thông | Đồ thị có hướng có trọng số G = (V, E, w); đường một chiều, cạnh song song; trọng số là độ dài hoặc thời gian. |
| `1.6` BFS/DFS | Chỉ đúng với đồ thị không trọng số; dùng làm mốc so sánh. |
| `1.7` Dijkstra | Ý tưởng tham lam, mã giả, độ phức tạp O((V + E) log V) với heap nhị phân, điều kiện trọng số không âm. |
| `1.8` A\* | f = g + h, heuristic Haversine, định nghĩa chấp nhận được và nhất quán, vì sao vẫn tối ưu. |
| `1.9` Bidirectional | 2 hướng tìm kiếm, điều kiện dừng, vì sao duyệt ít hơn (2 "hình tròn" bán kính r/2 thay vì 1 hình tròn bán kính r). |
| `1.10` CH, ALT | CH: tiền xử lý co node, thêm cạnh tắt, truy vấn 2 chiều chỉ đi "lên". ALT: chọn mốc (landmark), dùng bất đẳng thức tam giác làm heuristic. OSRM, GraphHopper dùng các kỹ thuật này. |
| `1.12` Bảng so sánh | Cột: thuật toán, độ phức tạp, cần tiền xử lý?, tối ưu?, ưu điểm, nhược điểm, ứng dụng. |

---

## 3. TV4 – FE: Bản đồ

**Phụ trách:** `FE/src/main.jsx`, `FE/src/App.jsx` (bố cục và trạng thái), `FE/src/App.css` (phần bố cục), `FE/src/constants.js`, `FE/src/components/MapView.jsx`, mở rộng `3.6` (animation, tìm địa chỉ). Báo cáo `1.11` và chụp hình giao diện.

**Kết quả cần đạt:** bản đồ căn theo quận, click 2 lần chọn điểm đi (xanh lá) và điểm đến (đỏ), kéo thả được marker, vẽ đường đi, vẽ node đã duyệt, vẽ khung bao quận.

### Bước 0. Bật dữ liệu giả

Trong `FE/.env` đặt `VITE_USE_MOCK=true`, chạy lại `npm run dev`. `client.js` sẽ trả dữ liệu giả đúng định dạng API, không cần BE.

### Bước 1. `main.jsx`

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import 'leaflet/dist/leaflet.css'   // thiếu dòng này bản đồ sẽ bị vỡ
import App from './App.jsx'
import './App.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

### Bước 2. `constants.js` (làm sớm, push trước để TV5 dùng)

```js
// Tên hiển thị và màu của từng thuật toán, dùng chung cho bản đồ, bảng số liệu, biểu đồ
export const ALGORITHMS = {
  dijkstra: { label: 'Dijkstra', color: '#e8590c' },
  astar: { label: 'A*', color: '#1971c2' },
}

export const formatDistance = (m) => (m >= 1000 ? `${(m / 1000).toFixed(2)} km` : `${Math.round(m)} m`)
```

### Bước 3. `App.jsx`: trạng thái và bố cục

`App.jsx` giữ toàn bộ trạng thái, truyền xuống component theo bảng props ở mục 0.6.

```jsx
import { useEffect, useState } from 'react'
import { compareRoutes, findRoute, getGraphInfo } from './api/client.js'
import CompareChart from './components/CompareChart.jsx'
import ControlPanel from './components/ControlPanel.jsx'
import MapView from './components/MapView.jsx'
import StatsPanel from './components/StatsPanel.jsx'

export default function App() {
  const [graphInfo, setGraphInfo] = useState(null)
  const [start, setStart] = useState(null) // { lat, lng }
  const [end, setEnd] = useState(null)
  const [algo, setAlgo] = useState('astar')
  const [results, setResults] = useState([]) // 1 phần tử khi Tìm đường, 2 khi So sánh
  const [showVisited, setShowVisited] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    getGraphInfo().then(setGraphInfo).catch((e) => setError(e.message))
  }, [])

  // Click lần 1 đặt điểm đi, lần 2 đặt điểm đến, lần 3 chọn lại từ đầu
  function handleMapClick(latlng) {
    if (!start || end) {
      setStart(latlng)
      setEnd(null)
    } else {
      setEnd(latlng)
    }
    setResults([])
  }

  async function run(request) {
    setLoading(true)
    setError(null)
    try {
      setResults(await request())
    } catch (e) {
      setResults([])
      setError(e.message) // client.js đã đổi lỗi của BE thành câu tiếng Việt
    } finally {
      setLoading(false)
    }
  }

  const handleFind = () => run(async () => [await findRoute(algo, start, end)])
  const handleCompare = () => run(async () => (await compareRoutes(start, end)).results)
  const handleClear = () => {
    setStart(null)
    setEnd(null)
    setResults([])
    setError(null)
  }

  return (
    <div className="app">
      <main className="map-area">
        {graphInfo ? (
          <MapView
            graphInfo={graphInfo}
            start={start}
            end={end}
            results={results}
            showVisited={showVisited}
            onMapClick={handleMapClick}
            onStartMove={(p) => { setStart(p); setResults([]) }}
            onEndMove={(p) => { setEnd(p); setResults([]) }}
          />
        ) : (
          <p className="placeholder">{error || 'Đang tải bản đồ…'}</p>
        )}
      </main>
      <aside className="sidebar">
        <h1>Tìm đường trên bản đồ số</h1>
        <ControlPanel
          algo={algo}
          onAlgoChange={setAlgo}
          canRun={Boolean(graphInfo && start && end)}
          loading={loading}
          error={error}
          showVisited={showVisited}
          onShowVisitedChange={setShowVisited}
          onFind={handleFind}
          onCompare={handleCompare}
          onClear={handleClear}
        />
        <StatsPanel results={results} />
        {results.length > 1 && <CompareChart results={results} />}
      </aside>
    </div>
  )
}
```

- Chỉ render `MapView` **sau khi có `graphInfo`**: `MapContainer` của react-leaflet chỉ đọc vị trí ban đầu một lần lúc tạo, đổi prop sau đó không có tác dụng.
- Khi TV5 chưa xong các component, `import` file chỉ có chú thích sẽ làm build lỗi. Cách làm: TV5 merge trước bản khung 3 component (nhận đúng props, giao diện đơn giản) trong tuần 1. Trong lúc chờ, TV4 tạm comment các dòng import và thẻ tương ứng.

### Bước 4. `App.css`: 2 cột, điện thoại xếp dọc

```css
* { box-sizing: border-box; }
html, body, #root { height: 100%; margin: 0; }
body { font-family: system-ui, sans-serif; }

.app { display: flex; height: 100vh; }
.map-area { flex: 1; min-width: 0; }
.map { height: 100%; width: 100%; } /* Leaflet bắt buộc container phải có chiều cao */
.sidebar { width: 360px; overflow-y: auto; padding: 16px; border-left: 1px solid #ddd; }

@media (max-width: 768px) {
  .app { flex-direction: column; height: auto; }
  .map-area { height: 60vh; }
  .sidebar { width: 100%; border-left: none; }
}

.pin { border-radius: 50%; border: 2px solid #fff; box-shadow: 0 0 3px rgba(0, 0, 0, 0.5); }
.pin-start { background: #2f9e44; }
.pin-end { background: #e03131; }
.error { color: #c92a2a; }
```

Phần trang trí các ô trong bảng điều khiển do TV5 làm, thêm vào cuối file này.

### Bước 5. `MapView.jsx`

```jsx
import L from 'leaflet'
import { CircleMarker, LayerGroup, MapContainer, Marker, Polyline, Rectangle, TileLayer, useMapEvents } from 'react-leaflet'
import { ALGORITHMS } from '../constants.js'

// Icon mặc định của Leaflet bị mất ảnh khi build bằng Vite, dùng divIcon tô màu bằng CSS
const pin = (cls) => L.divIcon({ className: `pin ${cls}`, iconSize: [18, 18], iconAnchor: [9, 9] })
const START_ICON = pin('pin-start')
const END_ICON = pin('pin-end')

function ClickHandler({ onClick }) {
  useMapEvents({ click: (e) => onClick({ lat: e.latlng.lat, lng: e.latlng.lng }) })
  return null
}

function DraggablePin({ position, icon, onMove }) {
  return (
    <Marker
      position={position}
      icon={icon}
      draggable
      eventHandlers={{ dragend: (e) => onMove(e.target.getLatLng()) }}
    />
  )
}

export default function MapView({ graphInfo, start, end, results, showVisited, onMapClick, onStartMove, onEndMove }) {
  const [south, west, north, east] = graphInfo.bbox
  const bounds = [[south, west], [north, east]]
  // Vẽ thuật toán duyệt nhiều node trước, để thuật toán duyệt ít nằm đè lên trên
  const ordered = [...results].sort((a, b) => b.visited_count - a.visited_count)

  return (
    // preferCanvas: vẽ hàng nghìn CircleMarker bằng canvas cho mượt
    <MapContainer bounds={bounds} preferCanvas className="map">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Rectangle bounds={bounds} interactive={false} pathOptions={{ color: '#555', weight: 1, dashArray: '6 6', fill: false }} />
      <ClickHandler onClick={onMapClick} />

      {/* Đổi key khi danh sách thuật toán đổi (Tìm đường -> So sánh) để Leaflet vẽ lại đúng thứ tự */}
      <LayerGroup key={ordered.map((r) => r.algorithm).join()}>
        {showVisited &&
          ordered.map((r) =>
            r.visited.map((p, i) => (
              <CircleMarker
                key={`${r.algorithm}-${i}`}
                center={p}
                radius={2.5}
                interactive={false}
                pathOptions={{ stroke: false, fillColor: ALGORITHMS[r.algorithm].color, fillOpacity: 0.35 }}
              />
            )),
          )}

        {ordered.map((r, i) => (
          <Polyline
            key={r.algorithm}
            positions={r.path}
            interactive={false}
            // Khi so sánh, 2 đường thường trùng nhau: đường vẽ trước dày hơn để vẫn thấy cả 2 màu
            pathOptions={{ color: ALGORITHMS[r.algorithm].color, weight: ordered.length > 1 && i === 0 ? 10 : 5 }}
          />
        ))}
      </LayerGroup>

      {start && <DraggablePin position={start} icon={START_ICON} onMove={onStartMove} />}
      {end && <DraggablePin position={end} icon={END_ICON} onMove={onEndMove} />}
    </MapContainer>
  )
}
```

Giải thích các chỗ dễ sai:

- `bbox` từ BE là `[south, west, north, east]`, Leaflet cần `[[south, west], [north, east]]`.
- Tọa độ trong API luôn là `[lat, lng]`, đúng thứ tự Leaflet cần, không phải đảo.
- BE chỉ gửi tối đa 5000 node đã duyệt (lấy mẫu đều), nên `visited.length` có thể nhỏ hơn `visited_count`.
- Nếu thấy bản đồ xám hoặc không có chiều cao: kiểm tra đã import `leaflet.css` và `.map` có `height`.
- Gợi ý thêm: vẽ nét đứt nối điểm click với node đầu/cuối của `path`, vì BE bắt điểm click về node gần nhất nên đường đi không bắt đầu đúng chỗ click.

### Bước 6. Nối với BE thật

Đặt `VITE_USE_MOCK=false`, chạy BE (cần TV2, TV3 xong), chạy lại `npm run dev`. Thử: chọn 2 điểm, Tìm đường, So sánh, kéo marker, click ngoài khung (phải hiện lỗi "nằm ngoài vùng bản đồ"). Nếu trình duyệt báo lỗi CORS xem mục 6.

### Bước 7 (mở rộng, P3)

- **Animation duyệt node:** thêm state `step`, dùng `setInterval` (hoặc `requestAnimationFrame`) tăng dần `step`, vẽ `r.visited.slice(0, step)`. Thêm nút "Phát lại". Dừng timer trong hàm dọn dẹp của `useEffect`.
- **Tìm địa chỉ (Nominatim):** gọi `https://nominatim.openstreetmap.org/search?format=json&q=<địa chỉ>&viewbox=<west>,<north>,<east>,<south>&bounded=1` khi người dùng **bấm nút Tìm**. Chính sách của Nominatim: tối đa 1 yêu cầu/giây và **không được gợi ý tự động theo từng phím gõ**. Chọn kết quả thì đặt làm điểm đi hoặc điểm đến.
- **Chọn đoạn kẹt xe:** làm cùng TV2 khi có API `/api/traffic`.

### Báo cáo TV4 (`docs/bao-cao/1.11-he-thong-thuc-te.md`)

| Hệ thống | Nội dung nên có |
|---|---|
| OSRM | C++, dữ liệu OSM, thuật toán Contraction Hierarchies và Multi-Level Dijkstra, tự host được, có máy chủ demo công khai |
| GraphHopper | Java, dữ liệu OSM, CH và Landmarks (ALT), tùy biến hồ sơ phương tiện |
| Valhalla | C++, dữ liệu chia ô (tile) phân cấp, tính chi phí linh hoạt lúc truy vấn |
| Google Directions | Đóng, có dữ liệu giao thông thời gian thực, trả phí theo lượt gọi |

Thêm bảng so sánh (ngôn ngữ, thuật toán, nguồn dữ liệu, giấy phép, giao thông thời gian thực, tự host) và đoạn liên hệ với đề tài: các hệ thống trên đều dựa trên Dijkstra/A\* cộng tiền xử lý để nhanh hơn.

**Ảnh chụp cho báo cáo:** màn hình ban đầu, kết quả Dijkstra, kết quả A\*, So sánh có biểu đồ, trang benchmark, thông báo lỗi khi chọn ngoài vùng, giao diện trên điện thoại (DevTools, chế độ thiết bị di động).

---

## 4. TV5 – FE: Giao diện và đánh giá

**Phụ trách:** `ControlPanel.jsx`, `StatsPanel.jsx`, `CompareChart.jsx`, trang benchmark (`BenchmarkPanel.jsx`), bên BE thêm `GET /api/compare` và `GET /api/benchmark` (`2.5`), chạy đánh giá thực nghiệm (mục `4`). Báo cáo `1.13`.

### Bước 1. `ControlPanel.jsx`

```jsx
import { ALGORITHMS } from '../constants.js'

export default function ControlPanel({
  algo, onAlgoChange, canRun, loading, error,
  showVisited, onShowVisitedChange, onFind, onCompare, onClear,
}) {
  return (
    <section className="card">
      <fieldset>
        <legend>Thuật toán</legend>
        {Object.entries(ALGORITHMS).map(([key, { label }]) => (
          <label key={key}>
            <input type="radio" name="algo" checked={algo === key} onChange={() => onAlgoChange(key)} />
            {label}
          </label>
        ))}
      </fieldset>

      <button disabled={!canRun || loading} onClick={onFind}>Tìm đường</button>
      <button disabled={!canRun || loading} onClick={onCompare}>So sánh</button>
      <button disabled={loading} onClick={onClear}>Xóa</button>

      <label>
        <input type="checkbox" checked={showVisited} onChange={(e) => onShowVisitedChange(e.target.checked)} />
        Hiện node đã duyệt
      </label>

      {!canRun && <p>Click lên bản đồ để chọn điểm đi, rồi điểm đến.</p>}
      {loading && <p>Đang tìm đường…</p>}
      {error && <p className="error">{error}</p>}
    </section>
  )
}
```

### Bước 2. `StatsPanel.jsx`

```jsx
import { ALGORITHMS, formatDistance } from '../constants.js'

const ROWS = [
  ['Độ dài đường đi', (r) => formatDistance(r.distance_m)],
  ['Thời gian chạy', (r) => `${r.runtime_ms.toFixed(2)} ms`],
  ['Số node đã duyệt', (r) => r.visited_count.toLocaleString('vi-VN')],
]

export default function StatsPanel({ results }) {
  if (results.length === 0) return null
  return (
    <table>
      <thead>
        <tr>
          <th />
          {results.map((r) => <th key={r.algorithm}>{ALGORITHMS[r.algorithm].label}</th>)}
        </tr>
      </thead>
      <tbody>
        {ROWS.map(([label, format]) => (
          <tr key={label}>
            <th scope="row">{label}</th>
            {results.map((r) => <td key={r.algorithm}>{format(r)}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  )
}
```

Dùng `visited_count` (tổng thật), không dùng `visited.length` (đã bị lấy mẫu tối đa 5000).

### Bước 3. BE: `GET /api/compare` trong `routes.py`

Hàm `find_route` của nhóm trưởng đã làm hết phần kiểm tra tọa độ, bắt node gần nhất, đổi kết quả sang định dạng API. Chỉ cần gọi lại cho mỗi thuật toán. `CompareResult` đã có sẵn trong `schemas.py`, `compareRoutes()` đã có sẵn trong `client.js`.

```python
# Đầu file: sửa dòng import typing thành `from typing import Annotated, get_args`
# và thêm CompareResult vào dòng `from app.schemas import ...`


@router.get("/compare", response_model=CompareResult, responses=ERRORS)
def get_compare(
    request: Request,
    from_lat: float = Query(ge=-90, le=90),
    from_lng: float = Query(ge=-180, le=180),
    to_lat: float = Query(ge=-90, le=90),
    to_lng: float = Query(ge=-180, le=180),
):
    results = [find_route(request, algo, from_lat, from_lng, to_lat, to_lng) for algo in get_args(Algorithm)]
    return CompareResult(results=results)
```

Test: thêm vào `tests/test_api.py`, dùng lại fixture `client` có sẵn (đồ thị 3 node, thuật toán giả), nên test được **trước khi TV3 xong**:

```python
def test_compare_runs_all_algorithms(client):
    res = client.get("/api/compare", params=route_params())
    assert res.status_code == 200
    assert [r["algorithm"] for r in res.json()["results"]] == ["dijkstra", "astar"]


def test_compare_outside_map(client):
    assert client.get("/api/compare", params=route_params(to_lat=21.03, to_lng=105.85)).status_code == 400
```

### Bước 4. `CompareChart.jsx` (Recharts)

```jsx
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { ALGORITHMS } from '../constants.js'

function Metric({ title, data, dataKey }) {
  return (
    <div>
      <h3>{title}</h3>
      <ResponsiveContainer width="100%" height={160}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis />
          <Tooltip />
          <Bar dataKey={dataKey}>
            {data.map((d) => <Cell key={d.label} fill={d.color} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function CompareChart({ results }) {
  const data = results.map((r) => ({ ...r, ...ALGORITHMS[r.algorithm] }))
  return (
    <section>
      <h2>So sánh</h2>
      <Metric title="Số node đã duyệt" data={data} dataKey="visited_count" />
      <Metric title="Thời gian chạy (ms)" data={data} dataKey="runtime_ms" />
    </section>
  )
}
```

Có thể thêm một câu tóm tắt, ví dụ "A\* duyệt ít hơn X% số node so với Dijkstra". Việc vẽ 2 đường đi cùng lúc trên bản đồ do `MapView` (TV4) làm sẵn khi `results` có 2 phần tử.

### Bước 5. BE: `GET /api/benchmark?n=50&seed=42`

Chạy N cặp node ngẫu nhiên, mỗi cặp chạy mọi thuật toán. Thêm vào `schemas.py` (báo TV1 và cập nhật [05-dinh-dang-api.md](05-dinh-dang-api.md)):

```python
class BenchmarkRow(BaseModel):
    pair: int
    straight_m: float = Field(description="Khoảng cách đường chim bay giữa 2 điểm")
    algorithm: Algorithm
    distance_m: float
    runtime_ms: float
    visited_count: int


class BenchmarkSummary(BaseModel):
    algorithm: Algorithm
    avg_distance_m: float
    avg_runtime_ms: float
    avg_visited_count: float


class BenchmarkResult(BaseModel):
    """GET /api/benchmark"""

    pair_count: int
    summary: list[BenchmarkSummary]
    rows: list[BenchmarkRow]
```

Thêm vào `routes.py` (cần `import random`, `import statistics`, `from app.algorithms import ALGORITHMS`, `haversine`, `BenchmarkResult`):

```python
@router.get("/benchmark", response_model=BenchmarkResult, responses={503: ERRORS[503]})
def get_benchmark(request: Request, n: int = Query(50, ge=1, le=500), seed: int = 42):
    G = _graph(request)
    rng = random.Random(seed)  # cùng seed thì cùng các cặp điểm, chạy lại cho ra cùng bộ dữ liệu
    nodes = list(G.nodes)
    rows = []
    pair = 0
    attempts = 0
    while pair < n and attempts < n * 10:
        attempts += 1
        start, goal = rng.sample(nodes, 2)
        try:
            results = {name: run_algorithm(name, G, start, goal) for name in ALGORITHMS}
        except NoPathError:
            continue
        a, b = G.nodes[start], G.nodes[goal]
        straight_m = haversine(a["y"], a["x"], b["y"], b["x"])  # để chia nhóm gần/xa khi đánh giá
        for name, r in results.items():
            rows.append({
                "pair": pair,
                "straight_m": straight_m,
                "algorithm": name,
                "distance_m": r["distance_m"],
                "runtime_ms": r["runtime_ms"],
                "visited_count": r["visited_count"],
            })
        pair += 1

    summary = []
    for name in ALGORITHMS:
        mine = [r for r in rows if r["algorithm"] == name]
        if not mine:
            continue
        summary.append({
            "algorithm": name,
            "avg_distance_m": statistics.mean(r["distance_m"] for r in mine),
            "avg_runtime_ms": statistics.mean(r["runtime_ms"] for r in mine),
            "avg_visited_count": statistics.mean(r["visited_count"] for r in mine),
        })
    return {"pair_count": pair, "summary": summary, "rows": rows}
```

- Giới hạn `n <= 500` để một request không chạy quá lâu.
- Cố định `seed` để chạy lại ra cùng bộ cặp điểm, đưa vào báo cáo được.

Thêm hàm vào `FE/src/api/client.js` (và hàm giả tương ứng trong `mock.js`, báo TV1):

```js
/** GET /api/benchmark → { pair_count, summary: [...], rows: [...] } */
export const getBenchmark = (n = 50, seed = 42) =>
  USE_MOCK ? mock.getBenchmark(n, seed) : get('/api/benchmark', { n, seed })
```

### Bước 6. Trang benchmark (`BenchmarkPanel.jsx`)

Ô nhập số cặp điểm, nút Chạy, bảng trung bình, nút tải CSV để làm biểu đồ cho báo cáo. Đặt trong sidebar hoặc làm tab riêng, thống nhất với TV4.

```jsx
import { useState } from 'react'
import { getBenchmark } from '../api/client.js'
import { ALGORITHMS } from '../constants.js'

function downloadCsv(rows) {
  const header = 'pair,straight_m,algorithm,distance_m,runtime_ms,visited_count'
  const lines = rows.map((r) => [r.pair, r.straight_m, r.algorithm, r.distance_m, r.runtime_ms, r.visited_count].join(','))
  const blob = new Blob([[header, ...lines].join('\n')], { type: 'text/csv' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = 'benchmark.csv'
  a.click()
  URL.revokeObjectURL(a.href)
}

export default function BenchmarkPanel() {
  const [n, setN] = useState(50)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function run() {
    setLoading(true)
    setError(null)
    try {
      setData(await getBenchmark(n))
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <h2>Benchmark</h2>
      <label>
        Số cặp điểm <input type="number" min={1} max={500} value={n} onChange={(e) => setN(Number(e.target.value))} />
      </label>
      <button disabled={loading} onClick={run}>{loading ? 'Đang chạy…' : 'Chạy'}</button>
      {error && <p className="error">{error}</p>}
      {data && (
        <>
          <p>{data.pair_count} cặp điểm</p>
          <table>
            <thead>
              <tr><th>Thuật toán</th><th>Độ dài TB (m)</th><th>Thời gian TB (ms)</th><th>Node duyệt TB</th></tr>
            </thead>
            <tbody>
              {data.summary.map((s) => (
                <tr key={s.algorithm}>
                  <td>{ALGORITHMS[s.algorithm].label}</td>
                  <td>{s.avg_distance_m.toFixed(1)}</td>
                  <td>{s.avg_runtime_ms.toFixed(2)}</td>
                  <td>{Math.round(s.avg_visited_count)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={() => downloadCsv(data.rows)}>Tải CSV</button>
        </>
      )}
    </section>
  )
}
```

Có thể dùng lại `CompareChart` để vẽ cột trung bình: truyền mảng `summary` sau khi đổi tên trường cho khớp (`avg_visited_count` thành `visited_count`, `avg_runtime_ms` thành `runtime_ms`).

### Bước 7. Đánh giá thực nghiệm (mục `4` trong file 03)

1. Ghi lại cấu hình máy (CPU, RAM), số node/cạnh của bản đồ, số cặp điểm, `seed`.
2. Chạy benchmark 100 cặp (`n=100`, `seed=42`), tải CSV. Thời gian ở mức mili giây nên dễ nhiễu: tắt bớt ứng dụng nặng, chạy 2–3 lần với cùng `seed` rồi lấy trung bình hoặc trung vị.
3. Kiểm tra độ đúng: mỗi cặp, `distance_m` của Dijkstra và A\* phải bằng nhau (100% cặp).
4. Chia nhóm theo `straight_m`, ví dụ dưới 1 km, 1–2 km, trên 2 km. Mỗi nhóm tính: thời gian trung bình, số node duyệt trung bình, tỉ lệ A\*/Dijkstra, số cặp A\* nhanh hơn.
5. Vẽ biểu đồ (Excel, Google Sheets hoặc matplotlib từ file CSV): cột so sánh trung bình, cột theo nhóm khoảng cách, biểu đồ chấm "số node duyệt theo khoảng cách".
6. Đối chiếu 5–10 tuyến với Google Maps hoặc OSRM. OSRM demo: `https://router.project-osrm.org/route/v1/driving/{lng1},{lat1};{lng2},{lat2}?overview=false`, lấy `routes[0].distance` (mét). **Chú ý OSRM ghi kinh độ trước, vĩ độ sau.** Máy chủ demo chỉ dùng thử, gọi ít và chậm. Giải thích chênh lệch: OSRM có cấm rẽ, hồ sơ xe khác, phiên bản dữ liệu khác, và BE của mình bắt điểm click về node gần nhất.
7. Nhận xét: A\* nhanh hơn rõ khi 2 điểm xa nhau; khi 2 điểm gần nhau thì gần bằng Dijkstra. Số node duyệt giảm nhiều hơn thời gian chạy giảm, vì A\* tốn thêm chi phí tính Haversine cho mỗi node.

### Báo cáo TV5 (`docs/bao-cao/1.13-ket-qua-thuc-nghiem.md`)

Gồm: môi trường thử nghiệm, cách chọn cặp điểm, bảng tổng hợp, các biểu đồ, phân tích theo nhóm khoảng cách, đối chiếu OSRM/Google Maps, nhận xét. **Gửi các con số chính cho nhóm trưởng** để điền vào các chỗ `[...]` trong [bao-cao/1.14-ket-luan.md](bao-cao/1.14-ket-luan.md).

---

## 5. Việc còn lại của nhóm trưởng (TV1)

- [ ] Merge `feature/nhom-truong` vào `main` để mọi người bắt đầu (bỏ các file `BE/data/osmnx_cache/` ra khỏi nhánh trước khi merge).
- [ ] Điền họ tên vào bảng ở [04-phan-cong.md](04-phan-cong.md).
- [ ] Review từng PR: CI xanh, đúng định dạng API, không commit file lớn hay `.env`, có test.
- [ ] Cập nhật [05-dinh-dang-api.md](05-dinh-dang-api.md) khi thêm `/api/benchmark`, `/api/traffic`, Bidirectional.
- [ ] Tuần 3: ghép FE–BE, chạy lại kịch bản demo ở mục 6 của [03-chuc-nang-can-lam.md](03-chuc-nang-can-lam.md).
- [ ] Điền số liệu vào `1.14`, ghép báo cáo, làm slide, điều phối buổi demo.

---

## 6. Lỗi thường gặp

| Hiện tượng | Nguyên nhân | Cách sửa |
|---|---|---|
| FE báo "Không kết nối được backend" | BE chưa chạy hoặc sai `VITE_API_URL` | Chạy `uvicorn`, kiểm tra `FE/.env`, chạy lại `npm run dev` |
| Console trình duyệt báo lỗi CORS | Mở FE bằng `127.0.0.1` nhưng `CORS_ORIGINS` chỉ có `localhost` | Trong `BE/.env` đặt `CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173`, khởi động lại BE |
| API trả 503 "Server chưa nạp bản đồ" | `graph_loader.py` chưa xong | Chờ TV2 hoặc xem log BE |
| API `/api/route` trả 500 | Thuật toán còn `NotImplementedError` hoặc lỗi code | Đọc traceback trong terminal BE |
| API trả 400 "nằm ngoài vùng bản đồ" | Chọn điểm ngoài khung đứt nét | Chọn điểm trong khung |
| Lần đầu khởi động BE rất lâu | Đang tải bản đồ từ OSM | Chờ; lần sau đọc cache |
| Bản đồ xám, vỡ ô | Thiếu `import 'leaflet/dist/leaflet.css'` hoặc `.map` không có chiều cao | Xem mục 3, bước 1 và 4 |
| Marker không hiện ảnh | Icon mặc định của Leaflet bị lỗi đường dẫn khi build bằng Vite | Dùng `L.divIcon` như mục 3 |
| `ruff check` báo lỗi | Import thừa, sai thứ tự import... | `ruff check . --fix` |
| CI FE lỗi sau khi thêm thư viện | Quên commit `package-lock.json` | Commit cả `package-lock.json` |
| Sửa `.env` không có tác dụng | Vite và uvicorn chỉ đọc `.env` khi khởi động | Tắt và chạy lại |
| `git push` lên `main` bị từ chối | `main` chỉ nhận qua Pull Request | Push nhánh riêng rồi tạo PR |

---

## 7. Thế nào là "xong việc"

Một phần việc chỉ tính là xong khi:

- [ ] Code chạy được trên máy mình, đã thử với BE/FE thật (không chỉ dữ liệu giả).
- [ ] Có test (với phần BE), `ruff check .`, `pytest`, `npm run build` đều đạt.
- [ ] PR vào `main` có CI xanh và đã được nhóm trưởng merge.
- [ ] Đánh dấu `[x]` mục tương ứng trong [03-chuc-nang-can-lam.md](03-chuc-nang-can-lam.md).
- [ ] Nếu có đổi API: đã cập nhật [05-dinh-dang-api.md](05-dinh-dang-api.md).
- [ ] Có bản nháp phần báo cáo của mình trong `docs/bao-cao/`.
- [ ] Giải thích được code của mình cho cả nhóm trong buổi họp tuần.
