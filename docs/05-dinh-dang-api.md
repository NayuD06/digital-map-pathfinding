# Định dạng API (đã chốt)

Tài liệu này là **hợp đồng giữa BE và FE**. Code nguồn của định dạng nằm ở [`BE/app/schemas.py`](../BE/app/schemas.py), FE gọi qua [`FE/src/api/client.js`](../FE/src/api/client.js).

Muốn đổi định dạng thì báo nhóm trưởng, sửa cả `schemas.py`, `client.js`, `mock.js` và tài liệu này trong cùng một Pull Request.

Quy ước chung:
- Tọa độ luôn là `[lat, lng]` (vĩ độ trước, kinh độ sau), giống Leaflet.
- Độ dài tính bằng mét (`distance_m`), thời gian bằng mili giây (`runtime_ms`).
- Lỗi trả về `{"detail": "thông báo tiếng Việt"}`; FE hiển thị thẳng `detail`.

## `GET /health`

```json
{ "status": "ok" }
```

## `GET /api/graph/info`

```json
{
  "place_name": "District 1, Ho Chi Minh City, Vietnam",
  "node_count": 2481,
  "edge_count": 5683,
  "bbox": [10.7632, 106.6825, 10.7966, 106.7135],
  "center": [10.7769, 106.7009]
}
```

`bbox` là `[south, west, north, east]`.

## `GET /api/route`

| Tham số | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `algo` | `dijkstra` \| `astar` | không | mặc định `astar` |
| `from_lat`, `from_lng` | số | có | điểm đi |
| `to_lat`, `to_lng` | số | có | điểm đến |

Ví dụ: `/api/route?algo=dijkstra&from_lat=10.7735&from_lng=106.7004&to_lat=10.7870&to_lng=106.7050`

```json
{
  "algorithm": "dijkstra",
  "path": [[10.7735, 106.7004], [10.7741, 106.7010], [10.7870, 106.7050]],
  "visited": [[10.7735, 106.7004], [10.7738, 106.7001]],
  "distance_m": 1834.6,
  "runtime_ms": 4.21,
  "visited_count": 1290
}
```

- `path`: tọa độ các node trên đường đi, từ điểm đi tới điểm đến.
- `visited`: tọa độ node đã duyệt theo thứ tự duyệt. Nếu duyệt quá 5000 node, BE chỉ gửi 5000 điểm lấy đều; `visited_count` vẫn là tổng số thật.

| Mã lỗi | Khi nào |
|---|---|
| 400 | Tọa độ nằm ngoài khung bao bản đồ |
| 404 | Không có đường đi giữa 2 điểm |
| 422 | Thiếu tham số hoặc `algo` không hợp lệ (FastAPI tự trả) |
| 503 | Server chưa nạp bản đồ |

## `GET /api/compare` (TV5)

Cùng tham số với `/api/route` nhưng không có `algo`. Trả về kết quả của từng thuật toán:

```json
{ "results": [ { "algorithm": "dijkstra", "...": "..." }, { "algorithm": "astar", "...": "..." } ] }
```

TV5 thêm endpoint này vào `routes.py` bằng cách gọi lại hàm `find_route` cho mỗi thuật toán.

## Giao diện giữa các phần trong BE

`main.py` và `routes.py` (TV1) gọi các hàm dưới đây. Mỗi người cài phần của mình nhưng **giữ nguyên tên hàm, tham số và kiểu trả về**:

| Hàm | File | Người làm |
|---|---|---|
| `load_graph(place_name, cache_file)` → `MultiDiGraph` (node có `y`, `x`; cạnh có `length`) | `graph_loader.py` | TV2 |
| `graph_info(G, place_name)` → dict đúng `GraphInfo` | `graph_loader.py` | TV2 |
| `nearest_node(G, lat, lng)` → id node | `algorithms/utils.py` | TV2 |
| `dijkstra(G, start, goal)`, `astar(G, start, goal)` → dict kết quả, ném `NoPathError` khi không có đường | `algorithms/` | TV3 |

Dict kết quả của thuật toán:

```python
{
    "path": [node_id, ...],
    "distance_m": float,
    "visited_count": int,
    "visited_nodes": [node_id, ...],   # theo thứ tự duyệt
    "runtime_ms": float,
}
```

Khi các hàm trên chưa được cài (còn `NotImplementedError`), server vẫn khởi động được: `/health` trả `ok`, các API bản đồ trả 503.

## Làm FE khi chưa có BE

Đặt `VITE_USE_MOCK=true` trong `FE/.env`. `client.js` sẽ trả dữ liệu giả từ `src/api/mock.js`, đúng định dạng ở trên.
