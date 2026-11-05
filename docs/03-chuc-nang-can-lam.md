# Nội dung và chức năng cần làm

Danh sách công việc của dự án. Đánh dấu `[x]` khi hoàn thành.

Mức ưu tiên:
- **P1**: bắt buộc, cần có để demo
- **P2**: nên có, giúp báo cáo đầy đủ hơn
- **P3**: mở rộng, làm nếu còn thời gian

---

## 1. Nội dung báo cáo khảo sát

| # | Nội dung | Ưu tiên | Trạng thái |
|---|---|---|---|
| 1.1 | Khái niệm bản đồ số, vai trò trong ITS | P1 | [ ] |
| 1.2 | Mô hình dữ liệu bản đồ: node, edge, thuộc tính đường | P1 | [ ] |
| 1.3 | So sánh nguồn dữ liệu: OpenStreetMap, Google Maps, HERE, Mapbox, VietMap | P1 | [ ] |
| 1.4 | Hệ tọa độ WGS84, Web Mercator; tile map và vector tile | P2 | [ ] |
| 1.5 | Mô hình hóa mạng giao thông thành đồ thị có hướng, có trọng số | P1 | [ ] |
| 1.6 | Thuật toán BFS/DFS (làm mốc so sánh) | P2 | [ ] |
| 1.7 | Thuật toán Dijkstra: ý tưởng, mã giả, độ phức tạp | P1 | [ ] |
| 1.8 | Thuật toán A\*: heuristic Haversine, điều kiện heuristic chấp nhận được | P1 | [ ] |
| 1.9 | Bidirectional Dijkstra | P2 | [ ] |
| 1.10 | Giới thiệu Contraction Hierarchies, ALT | P3 | [ ] |
| 1.11 | Các hệ thống thực tế: OSRM, GraphHopper, Valhalla, Google Directions | P2 | [ ] |
| 1.12 | Bảng so sánh các thuật toán: độ phức tạp, ưu nhược điểm | P1 | [ ] |
| 1.13 | Kết quả thực nghiệm và nhận xét | P1 | [ ] |
| 1.14 | Kết luận và hướng phát triển | P1 | [ ] |

---

## 2. Chức năng Backend (`BE/`)

### 2.1 Cấu hình và khởi tạo — P1
- [x] `config.py`: đọc `PORT`, `PLACE_NAME`, `CORS_ORIGINS`, `GRAPH_BUFFER_KM`, `GRAPH_CACHE_PATH`, `GRAPH_BBOX`, `OVERPASS_URL`, `MYSQL_*` từ `.env`
- [x] `main.py`: tạo app FastAPI, bật CORS, gắn router `/api`
- [x] Endpoint `GET /health` trả về `{"status": "ok"}`

### 2.2 Tải và quản lý bản đồ — P1
- [x] `graph_loader.py`: tải mạng đường (mặc định toàn TP.HCM theo ranh giới mới, nới thêm 10 km) bằng `osmnx.graph_from_polygon(..., network_type="drive")`
- [x] Lưu cache ra file `.graphml`; lần chạy sau đọc từ file
- [x] Nạp đồ thị một lần khi khởi động server
- [x] `GET /api/graph/info`: trả về tên khu vực, số node, số cạnh, khung bao (bbox), tâm bản đồ
- [x] Bản đồ toàn TP.HCM: tính sẵn danh sách kề, tìm node gần nhất bằng NumPy, chỉ trả về FE tối đa 5.000 node đã duyệt (lấy mẫu đều), tự thử lại khi Overpass lỗi
- [x] Script `scripts/graph_from_pbf.py` dựng bản đồ từ file OSM của Geofabrik khi Overpass quá tải

**Kết quả cần đạt:** khởi động lần 2 không tải lại từ mạng, API trả đúng số node/cạnh.

### 2.3 Thuật toán — P1
- [x] `utils.py`:
  - [x] `haversine(lat1, lng1, lat2, lng2)` tính khoảng cách mét
  - [x] `reconstruct_path(parent, start, goal)` dựng lại đường đi
  - [x] `nearest_node(G, lat, lng)` tìm node gần tọa độ nhất
- [x] `dijkstra.py`: tự cài đặt bằng `heapq`, trọng số là `length` của cạnh
- [x] `astar.py`: tự cài đặt, heuristic Haversine tới đích
- [x] Cả 2 hàm trả về cùng một cấu trúc:
  ```python
  {
      "path": [node_id, ...],
      "distance_m": float,
      "visited_count": int,
      "visited_nodes": [node_id, ...],   # theo thứ tự duyệt
      "runtime_ms": float,
  }
  ```
- [x] Xử lý trường hợp không có đường đi (trả lỗi rõ ràng)

**Kết quả cần đạt:** Dijkstra và A\* cho cùng độ dài đường đi; A\* duyệt ít node hơn.

### 2.4 API tìm đường — P1
- [x] `schemas.py`: Pydantic models cho request và response
- [x] `GET /api/route?algo=dijkstra|astar&from_lat=&from_lng=&to_lat=&to_lng=`
  - Trả về đường đi dạng danh sách tọa độ `[[lat, lng], ...]`
  - Trả về tọa độ các node đã duyệt
  - Trả về độ dài, thời gian chạy, số node đã duyệt
- [x] Trả lỗi 400 khi tọa độ nằm ngoài quận, 404 khi không có đường

### 2.5 API so sánh — P2
- [x] `GET /api/compare?...`: chạy tất cả thuật toán trên cùng cặp điểm
- [x] `POST /api/benchmark?n=50&seed=`: chạy N cặp điểm ngẫu nhiên, trả về thống kê trung bình và từng dòng kết quả

### 2.6 Kiểm thử — P1
- [x] Test Dijkstra và A\* trên đồ thị nhỏ tự tạo (biết trước kết quả)
- [x] Test Dijkstra và A\* cho cùng độ dài trên bản đồ thật
- [x] Đối chiếu với `networkx.shortest_path_length` để kiểm tra độ đúng
- [x] Test trường hợp không có đường đi
- [x] Test lưu/đọc bản đồ, lịch sử, benchmark (SQLite trong bộ nhớ)

### 2.7 Lưu trữ MySQL — P2
- [x] `db.py`, `models.py`: tự tạo database và các bảng `maps`, `nodes`, `edges`, `route_queries`, `benchmark_runs`, `benchmark_results`
- [x] Nạp bản đồ từ MySQL khi khởi động; lần đầu chép bản đồ từ file/OSM vào MySQL
- [x] Lưu mỗi lần tìm đường; `GET /api/history`
- [x] Lưu kết quả benchmark (từng cặp điểm × thuật toán)
- [x] Chạy được khi không cấu hình MySQL (không lưu)

### 2.8 Mở rộng — P3
- [ ] Bidirectional Dijkstra (`algorithms/bidirectional.py`)
- [ ] Trọng số theo thời gian: dùng `osmnx.add_edge_speeds` và `add_edge_travel_times`
- [ ] Giả lập kẹt xe: `POST /api/traffic` tăng trọng số một số cạnh, `DELETE /api/traffic` đặt lại
- [ ] So sánh kết quả với OSRM public API

---

## 3. Chức năng Frontend (`FE/`)

### 3.1 Khởi tạo — P1
- [x] `main.jsx`: render `App`, import `leaflet/dist/leaflet.css`
- [x] `api/client.js`: các hàm `getGraphInfo()`, `findRoute()`, `compareRoutes()`, `getHistory()`, `runBenchmark()`, đọc `VITE_API_URL`
- [x] `App.jsx`: bố cục 2 cột (bản đồ, bảng điều khiển); trên điện thoại xếp dọc

### 3.2 Bản đồ — P1 (`MapView.jsx`)
- [x] Hiển thị bản đồ OSM, căn giữa theo tâm bản đồ lấy từ `/api/graph/info`
- [x] Click lần 1 đặt điểm đi (marker xanh lá), lần 2 đặt điểm đến (marker đỏ)
- [x] Kéo thả marker để đổi điểm
- [x] Vẽ đường đi bằng `Polyline`
- [x] Vẽ các node đã duyệt bằng `CircleMarker` nhỏ, mờ
- [x] Vẽ khung bao của bản đồ để người dùng biết vùng hỗ trợ

### 3.3 Bảng điều khiển — P1 (`ControlPanel.jsx`)
- [x] Chọn thuật toán: Dijkstra / A\*
- [x] Nút **Tìm đường**, **So sánh**, **Xóa**
- [x] Bật/tắt hiển thị node đã duyệt
- [x] Trạng thái đang tải và thông báo lỗi

### 3.4 Số liệu — P1 (`StatsPanel.jsx`)
- [x] Độ dài đường đi (m / km)
- [x] Thời gian chạy thuật toán (ms)
- [x] Số node đã duyệt

### 3.5 So sánh — P2 (`CompareChart.jsx`)
- [x] Vẽ 2 đường đi cùng lúc với 2 màu khác nhau
- [x] Biểu đồ cột Recharts: thời gian chạy và số node duyệt của từng thuật toán
- [x] Tab Benchmark (`BenchmarkPanel.jsx`): nhập số cặp điểm và seed, biểu đồ trung bình, biểu đồ số node duyệt theo khoảng cách, tải CSV

### 3.6 Lịch sử — P2 (`HistoryPanel.jsx`)
- [x] Hiện 10 lần tìm đường gần nhất (chỉ khi có database)
- [x] Click một dòng để đặt lại 2 điểm và chạy lại

### 3.7 Mở rộng — P3
- [ ] Hiệu ứng duyệt node theo thời gian (animation) để thấy cách thuật toán lan ra
- [ ] Chọn đoạn đường để đánh dấu kẹt xe
- [ ] Ô tìm kiếm địa chỉ (geocoding qua Nominatim)

---

## 4. Đánh giá thực nghiệm — P1

- [x] Chọn 50–100 cặp điểm ngẫu nhiên trên bản đồ (tab Benchmark, ghi lại seed để chạy lại được)
- [x] Ghi lại: độ dài, thời gian chạy, số node duyệt cho từng thuật toán (bảng `benchmark_results`, file CSV)
- [ ] Vẽ biểu đồ so sánh, đưa vào báo cáo
- [ ] Đối chiếu một số tuyến với Google Maps hoặc OSRM
- [ ] Nhận xét: khi nào A\* nhanh hơn rõ rệt, khi nào gần bằng Dijkstra

---

## 5. Sản phẩm cần nộp

- [ ] Mã nguồn trên GitHub, CI chạy đạt
- [ ] Báo cáo khảo sát
- [ ] Slide thuyết trình
- [ ] Video hoặc kịch bản demo
- [ ] README hướng dẫn cài đặt và chạy

---

## 6. Kịch bản demo đề xuất

1. Mở ứng dụng, giới thiệu bản đồ TP.HCM và số node/cạnh của đồ thị.
2. Chọn 2 điểm xa nhau, chạy **Dijkstra**: xem đường đi và vùng node đã duyệt rộng.
3. Chạy **A\*** trên cùng 2 điểm: cùng đường đi, vùng duyệt hẹp hơn hẳn.
4. Bấm **So sánh**: xem biểu đồ thời gian chạy và số node duyệt.
5. (Nếu có) Đánh dấu kẹt xe một đoạn đường, chạy lại: tuyến đường đổi hướng.
