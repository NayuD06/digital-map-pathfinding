# Phân công nhóm

Nhóm 5 người. Mỗi người phụ trách **một phần code** và **một phần báo cáo** liên quan đến phần code đó, để ai cũng hiểu và thuyết trình được phần mình làm.

Mã công việc (ví dụ `2.3`) tham chiếu tới [03-chuc-nang-can-lam.md](03-chuc-nang-can-lam.md).

> Điền tên thật vào cột **Họ tên**.

## 1. Tổng quan vai trò

| # | Họ tên | Vai trò | Code phụ trách | Báo cáo phụ trách |
|---|---|---|---|---|
| TV1 | *(Nhóm trưởng)* | Quản lý, tích hợp FE–BE | Cấu hình BE, API, CI | Kết luận, tổng hợp báo cáo, slide |
| TV2 | | BE – Dữ liệu bản đồ | Tải bản đồ, cache, trọng số | Tổng quan bản đồ số |
| TV3 | | BE – Thuật toán | Dijkstra, A\*, test | Lý thuyết thuật toán |
| TV4 | | FE – Bản đồ | Leaflet, chọn điểm, vẽ đường | Hệ thống tìm đường thực tế |
| TV5 | | FE – Giao diện & Đánh giá | Bảng điều khiển, biểu đồ, benchmark | Kết quả thực nghiệm |

## 2. Chi tiết từng người

### TV1 – Nhóm trưởng
**Quản lý**
- Chia việc, theo dõi tiến độ, họp nhóm hằng tuần
- Review và merge Pull Request vào `main`
- Giữ CI luôn đạt

**Code**
- `2.1` Cấu hình và khởi tạo BE (`config.py`, `main.py`, `/health`)
- `2.4` Định nghĩa `schemas.py` và API `/api/route`. **Chốt định dạng API sớm** để BE và FE làm song song
- `3.1` Phần `api/client.js` bên FE (thống nhất với API)
- Tích hợp FE–BE, sửa lỗi khi ghép

**Báo cáo**
- `1.14` Kết luận và hướng phát triển
- Ghép báo cáo, thống nhất định dạng
- Làm slide, điều phối buổi demo

### TV2 – BE: Dữ liệu bản đồ
**Code**
- `2.2` `graph_loader.py`: tải bản đồ quận bằng OSMnx, cache `.graphml`, nạp khi khởi động
- `2.2` API `/api/graph/info`
- `2.3` Hàm `nearest_node` trong `utils.py`
- `2.7` Trọng số theo thời gian, giả lập kẹt xe (mở rộng)

**Báo cáo**
- `1.1` Khái niệm bản đồ số, vai trò trong ITS
- `1.2` Mô hình dữ liệu bản đồ
- `1.3` So sánh nguồn dữ liệu bản đồ
- `1.4` Hệ tọa độ, tile map

### TV3 – BE: Thuật toán
**Code**
- `2.3` `haversine`, `reconstruct_path` trong `utils.py`
- `2.3` `dijkstra.py`, `astar.py`
- `2.6` Toàn bộ test trong `tests/`
- `2.7` Bidirectional Dijkstra (mở rộng)

**Báo cáo**
- `1.5` Mô hình hóa mạng giao thông thành đồ thị
- `1.6`–`1.10` Các thuật toán: BFS/DFS, Dijkstra, A\*, Bidirectional, CH/ALT
- `1.12` Bảng so sánh thuật toán

### TV4 – FE: Bản đồ
**Code**
- `3.1` `main.jsx`, bố cục `App.jsx`
- `3.2` `MapView.jsx`: hiển thị bản đồ, chọn điểm, kéo thả marker, vẽ đường đi, vẽ node đã duyệt, khung bao quận
- `3.6` Animation duyệt node, tìm kiếm địa chỉ (mở rộng)

**Báo cáo**
- `1.11` Các hệ thống tìm đường thực tế: OSRM, GraphHopper, Valhalla, Google Directions
- Chụp hình giao diện cho báo cáo

### TV5 – FE: Giao diện & Đánh giá
**Code**
- `3.3` `ControlPanel.jsx`
- `3.4` `StatsPanel.jsx`
- `3.5` `CompareChart.jsx`, trang benchmark
- `2.5` API `/api/compare` và `/api/benchmark` bên BE

**Báo cáo**
- `4` Chạy đánh giá thực nghiệm, vẽ biểu đồ
- `1.13` Kết quả thực nghiệm và nhận xét

## 3. Phụ thuộc giữa các phần

```
TV1 chốt định dạng API (schemas.py)
   │
   ├──► TV2 tải bản đồ ──► TV3 chạy thuật toán trên bản đồ thật ──► TV1 nối vào /api/route
   │                                                                   │
   └──► TV4, TV5 làm FE với dữ liệu giả (mock) ───────────────────────►┴──► Ghép FE–BE
                                                                            │
                                                              TV5 chạy đánh giá thực nghiệm
```

- TV3 viết và test thuật toán trên **đồ thị nhỏ tự tạo** trước, không cần chờ TV2.
- TV4, TV5 dùng **dữ liệu giả** đúng định dạng API để làm giao diện trước, không cần chờ BE.

## 4. Kế hoạch theo tuần

| Tuần | TV1 | TV2 | TV3 | TV4 | TV5 |
|---|---|---|---|---|---|
| 1 | Chốt API, cấu hình BE | Tải và cache bản đồ | Dijkstra trên đồ thị nhỏ | Hiển thị bản đồ, chọn điểm | Khung bảng điều khiển |
| 2 | `/api/route`, `client.js` | `/api/graph/info`, `nearest_node` | A\*, viết test | Vẽ đường đi, node đã duyệt | Bảng số liệu |
| 3 | Ghép FE–BE | Viết báo cáo phần bản đồ | Test trên bản đồ thật | Hoàn thiện bản đồ | `/api/compare`, biểu đồ |
| 4 | Review, sửa lỗi | Mở rộng: kẹt xe | Viết báo cáo thuật toán | Viết báo cáo hệ thống thực tế | Benchmark, đánh giá |
| 5 | Ghép báo cáo, slide | Hỗ trợ demo | Mở rộng: Bidirectional | Mở rộng: animation | Viết báo cáo kết quả |
| 6 | Tổng duyệt demo | Tổng duyệt | Tổng duyệt | Tổng duyệt | Tổng duyệt |

Có thể co giãn theo thời hạn thực tế của môn học.

## 5. Quy trình làm việc với Git

1. Luôn cập nhật `main` trước khi làm:
   ```bash
   git checkout main
   git pull origin main
   ```
2. Tạo nhánh riêng cho mỗi chức năng:
   ```bash
   git checkout -b feature/ten-chuc-nang
   ```
   Ví dụ: `feature/astar`, `feature/map-view`, `docs/bao-cao-thuat-toan`
3. Commit nhỏ, nội dung rõ ràng, ví dụ `Thêm thuật toán A* với heuristic Haversine`.
4. Push nhánh và tạo Pull Request vào `main`.
5. CI phải đạt và **nhóm trưởng review** trước khi merge.
6. **Không push thẳng lên `main`.**

## 6. Quy định chung

- Mỗi người cập nhật trạng thái `[x]` trong [03-chuc-nang-can-lam.md](03-chuc-nang-can-lam.md) khi xong việc.
- Báo ngay cho nhóm khi bị kẹt quá 1 ngày.
- Họp nhóm 1 lần/tuần: mỗi người báo đã làm gì, sắp làm gì, đang vướng gì.
- Ai cũng phải chạy được toàn bộ dự án trên máy mình và hiểu luồng chính để trả lời khi bảo vệ.
