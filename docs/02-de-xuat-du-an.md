# Đề xuất dự án: Khảo sát bản đồ số và thuật toán tìm đường

## 1. Mục tiêu

- Khảo sát các nguồn bản đồ số và cách mô hình hóa mạng lưới giao thông thành đồ thị.
- Tìm hiểu và so sánh các thuật toán tìm đường ngắn nhất.
- Xây dựng ứng dụng web demo: tìm đường bằng **Dijkstra** và **A\*** trên bản đồ một quận thật từ OpenStreetMap.
- Đánh giá thực nghiệm hiệu năng các thuật toán.

## 2. Nội dung đề tài

### Phần A: Khảo sát (báo cáo)

1. **Tổng quan bản đồ số**
   - Khái niệm bản đồ số, vai trò trong hệ thống giao thông thông minh (ITS)
   - Mô hình dữ liệu: node, edge, thuộc tính đường (một chiều, tốc độ, loại đường)
   - So sánh nguồn dữ liệu: OpenStreetMap, Google Maps, HERE, Mapbox, bản đồ Việt Nam (Vietbando, VietMap)
   - Hệ tọa độ (WGS84, Web Mercator), tile map, vector tile
2. **Mô hình hóa mạng lưới giao thông thành đồ thị**
   - Đồ thị có hướng, có trọng số
   - Trọng số có thể là khoảng cách, thời gian, hoặc mức độ kẹt xe
3. **Các thuật toán tìm đường**
   - BFS/DFS (làm mốc so sánh)
   - **Dijkstra**
   - **A\*** với heuristic Haversine
   - Bidirectional Dijkstra
   - Giới thiệu Contraction Hierarchies và ALT (kỹ thuật dùng trong OSRM, GraphHopper)
   - Bảng so sánh độ phức tạp, ưu nhược điểm
4. **Các hệ thống tìm đường thực tế:** OSRM, GraphHopper, Valhalla, Google Directions API

### Phần B: Ứng dụng demo

- Tải bản đồ một quận (mặc định **Quận 1, TP.HCM**) từ OpenStreetMap
- Click chọn điểm đi và điểm đến trên bản đồ
- Chọn thuật toán: Dijkstra hoặc A\*
- Hiển thị:
  - Đường đi tìm được
  - Các node đã duyệt (thấy rõ A\* duyệt ít hơn Dijkstra)
  - Số liệu: độ dài, thời gian chạy, số node đã duyệt
- Chức năng so sánh 2 thuật toán trên cùng cặp điểm

### Phần C: Đánh giá

- Chạy 50–100 cặp điểm ngẫu nhiên, so sánh thời gian chạy và số node duyệt
- Đối chiếu kết quả với OSRM hoặc Google Maps để kiểm tra độ đúng

### Mở rộng (nếu còn thời gian)

- Bidirectional Dijkstra
- Giả lập kẹt xe: tăng trọng số một số đoạn đường, quan sát tuyến đường thay đổi
- So sánh với OSRM
- Deploy: BE lên Render, FE lên Vercel

## 3. Công nghệ

### Backend

| Thành phần | Công nghệ | Lý do |
|---|---|---|
| Ngôn ngữ | Python 3.12 | Hệ sinh thái xử lý bản đồ, đồ thị mạnh |
| Web API | FastAPI + Uvicorn | Nhẹ, tự sinh tài liệu API tại `/docs` |
| Dữ liệu bản đồ | OSMnx | Tải mạng đường theo tên quận |
| Đồ thị | NetworkX | Định dạng OSMnx trả về sẵn |
| Thuật toán | Tự cài đặt bằng `heapq` | Đếm được số node duyệt, giải thích được khi bảo vệ |
| Cấu hình | pydantic-settings + `.env` | Đổi port, quận, CORS không cần sửa code |
| Kiểm thử | pytest | Kiểm tra Dijkstra và A\* cho cùng kết quả |

> Nên dùng **Python 3.12**. Python 3.14 có thể chưa có bản cài đặt sẵn cho một số thư viện địa lý mà OSMnx cần (shapely, pyproj…).

### Frontend

| Thành phần | Công nghệ | Lý do |
|---|---|---|
| Framework | React 18 + Vite | Khởi tạo nhanh, tự tải lại khi sửa code |
| Bản đồ | Leaflet + react-leaflet | Đơn giản, không cần API key |
| Lớp nền | Tile OpenStreetMap | Miễn phí |
| Biểu đồ | Recharts | Vẽ biểu đồ so sánh hiệu năng |
| Gọi API | `fetch` | Có sẵn trong trình duyệt |

### Chạy riêng FE và BE

- BE chạy port **8000**, FE chạy port **5173**
- BE bật CORS cho FE
- FE đọc địa chỉ BE từ biến `VITE_API_URL` trong `.env`

Chi tiết cấu trúc xem [01-cau-truc-du-an.md](01-cau-truc-du-an.md).

## 4. Kế hoạch thực hiện

| Giai đoạn | Công việc | Kết quả |
|---|---|---|
| 1 | Dựng khung dự án, cấu hình FE/BE | Khung thư mục, chạy được 2 phần ✅ (khung đã có) |
| 2 | BE: tải bản đồ quận bằng OSMnx, cache file | API `/api/graph/info` |
| 3 | BE: cài đặt Dijkstra, A\*, viết test | API `/api/route` |
| 4 | FE: hiển thị bản đồ, chọn điểm, vẽ đường đi | Demo tìm đường hoạt động |
| 5 | FE: hiển thị node đã duyệt, số liệu, so sánh | Màn hình so sánh thuật toán |
| 6 | Đánh giá thực nghiệm, vẽ biểu đồ | Số liệu cho báo cáo |
| 7 | Viết báo cáo khảo sát, chuẩn bị slide | Báo cáo và slide hoàn chỉnh |
| 8 | (Tùy chọn) Mở rộng: kẹt xe, bidirectional, deploy | Điểm cộng |

## 5. Hướng dẫn bắt đầu cho thành viên

1. Clone repo:
   ```bash
   git clone https://github.com/NayuD06/digital-map-pathfinding.git
   ```
2. Cài **Python 3.12** và **Node.js 20 trở lên**.
3. Làm theo phần "Cách chạy" trong [01-cau-truc-du-an.md](01-cau-truc-du-an.md).
4. Mỗi chức năng làm trên một nhánh riêng, ví dụ `feature/astar`, rồi tạo Pull Request vào `main`.
