# Cấu trúc dự án

Dự án gồm 2 phần chạy **độc lập, mỗi phần một port**:

| Phần | Thư mục | Công nghệ | Port |
|---|---|---|---|
| Backend | `BE/` | Python 3.12, FastAPI, OSMnx, NetworkX, NumPy, SQLAlchemy | 8000 |
| Frontend | `FE/` | React 18, Vite, Leaflet, Recharts | 5173 |
| Database | MySQL trên máy | MySQL 8 (không bắt buộc) | 3306 |

FE gọi BE qua HTTP. BE bật CORS cho phép `http://localhost:5173`.

## Cây thư mục

```
digital-map-pathfinding/
├── .gitignore
├── README.md
├── .github/
│   └── workflows/
│       ├── backend-ci.yml        # CI cho BE: ruff, kiểm tra cú pháp, pytest
│       └── frontend-ci.yml       # CI cho FE: npm ci, build, lưu bản build
├── docs/
│   ├── 01-cau-truc-du-an.md      # Tài liệu này
│   └── 02-de-xuat-du-an.md       # Đề xuất nội dung, công nghệ, kế hoạch
│
├── BE/
│   ├── .env.example              # Mẫu cấu hình (copy thành .env)
│   ├── README.md                 # Hướng dẫn chạy BE
│   ├── requirements.txt          # Thư viện Python
│   ├── app/
│   │   ├── main.py               # Khởi tạo FastAPI, bật CORS, gắn router
│   │   ├── config.py             # Đọc cấu hình từ .env
│   │   ├── graph_loader.py       # Nạp bản đồ: MySQL → file .graphml → tải từ OSM
│   │   ├── db.py                 # Kết nối database, tự tạo database và bảng
│   │   ├── models.py             # Các bảng (SQLAlchemy ORM)
│   │   ├── repository.py         # Đọc/ghi bản đồ, lịch sử, benchmark
│   │   ├── benchmark.py          # Chạy N cặp điểm ngẫu nhiên, tính thống kê
│   │   ├── schemas.py            # Pydantic models cho request/response
│   │   ├── api/
│   │   │   └── routes.py         # Các endpoint /api/...
│   │   └── algorithms/
│   │       ├── __init__.py       # run_algorithm: chạy 5 lần, lấy lần nhanh nhất
│   │       ├── dijkstra.py       # Thuật toán Dijkstra (tự cài đặt)
│   │       ├── astar.py          # Thuật toán A* (heuristic Haversine)
│   │       └── utils.py          # Haversine, dựng lại đường đi, tìm node gần nhất
│   ├── data/                     # Nơi lưu file bản đồ cache (không push lên git)
│   └── tests/
│       ├── test_algorithms.py    # Kiểm thử thuật toán bằng pytest
│       └── test_storage.py       # Kiểm thử lưu trữ (SQLite trong bộ nhớ)
│
└── FE/
    ├── .env.example              # VITE_API_URL=http://localhost:8000
    ├── README.md                 # Hướng dẫn chạy FE
    ├── index.html
    ├── package.json
    ├── package-lock.json         # Khóa phiên bản thư viện (CI dùng npm ci)
    ├── vite.config.js            # Cấu hình Vite, port 5173
    ├── public/                   # File tĩnh
    └── src/
        ├── main.jsx              # Điểm khởi chạy React
        ├── App.jsx               # Bố cục: bản đồ bên trái, bảng điều khiển bên phải
        ├── App.css
        ├── constants.js          # Tên, màu của từng thuật toán; định dạng khoảng cách
        ├── api/
        │   └── client.js         # Hàm gọi API backend
        └── components/
            ├── MapView.jsx       # Bản đồ Leaflet, chọn điểm, vẽ đường đi
            ├── ControlPanel.jsx  # Chọn thuật toán, nút Tìm đường / So sánh
            ├── StatsPanel.jsx    # Độ dài, thời gian chạy, số node đã duyệt
            ├── CompareChart.jsx  # Biểu đồ so sánh hiệu năng
            ├── HistoryPanel.jsx  # Lịch sử tìm đường (khi có database)
            └── BenchmarkPanel.jsx # Tab Benchmark: chạy N cặp điểm, biểu đồ, tải CSV
```

## Cấu hình môi trường

**`BE/.env`**
```
PORT=8000
PLACE_NAME=Ho Chi Minh City, Vietnam
CORS_ORIGINS=http://localhost:5173
GRAPH_BUFFER_KM=10
GRAPH_CACHE_PATH=
GRAPH_BBOX=
OVERPASS_URL=
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=digital_map
```

- Mặc định BE dùng bản đồ **toàn TP.HCM theo ranh giới mới** (từ 7/2025, gồm cả Bình Dương và Bà Rịa – Vũng Tàu cũ). Xem phần [Bản đồ toàn TP.HCM](#bản-đồ-toàn-tphcm).
- Lần chạy đầu BE tải bản đồ từ OpenStreetMap rồi lưu thành file `.graphml`. Những lần sau BE đọc từ file này (hoặc từ MySQL nếu có).
- `GRAPH_BUFFER_KM` nới ranh giới thêm N km sang tỉnh lân cận, để tìm được những tuyến phải đi qua tỉnh khác (TP.HCM → Vũng Tàu đi qua Đồng Nai). Chạy với một quận thì đặt `0`.
- `GRAPH_CACHE_PATH` để trống thì mỗi bản đồ có một file riêng đặt theo tên và độ nới, ví dụ `data/ho-chi-minh-city-vietnam-10-km.graphml`, `data/district-1-ho-chi-minh-city-vietnam.graphml`. Vì vậy đổi qua lại `PLACE_NAME`, `GRAPH_BUFFER_KM` không cần xóa file nào. Nếu tự đặt `GRAPH_CACHE_PATH` thì khi đổi hai biến này phải xóa file đó để BE tải lại.
- `OVERPASS_URL`: máy chủ Overpass dùng để tải bản đồ, để trống thì dùng `overpass-api.de`.
- `GRAPH_BBOX` là phương án dự phòng khi không tìm được ranh giới theo tên (dạng `west,south,east,north`). Từ 7/2025 Việt Nam bỏ cấp quận, nên trên OSM, Quận 1 hiện là ranh giới "historic"; hiện vẫn tải theo tên được.
- Sau khi nạp, BE chỉ giữ **thành phần liên thông mạnh lớn nhất** của đồ thị. Lý do: đường bị cắt ở ranh giới khu vực để lại những node một chiều, chỉ đi vào hoặc chỉ đi ra được. Với TP.HCM, bước này cũng bỏ Côn Đảo vì không có đường bộ nối với đất liền.

**`FE/.env`**
```
VITE_API_URL=http://localhost:8000
```

File `.env` thật không được đưa lên git, chỉ có `.env.example`.

## Bản đồ toàn TP.HCM

**Phạm vi.** Ranh giới TP.HCM mới trên OpenStreetMap (gồm TP.HCM cũ, Bình Dương, Bà Rịa – Vũng Tàu), nới thêm `GRAPH_BUFFER_KM` = 10 km. Cần nới vì đường bộ từ trung tâm ra Vũng Tàu (cao tốc Long Thành, QL51) đi qua Long Thành, Nhơn Trạch của Đồng Nai. Nếu cắt đúng ranh giới thì Vũng Tàu bị tách khỏi phần còn lại và bị bỏ ở bước giữ thành phần liên thông mạnh lớn nhất. Vì vậy bản đồ có thêm một dải khoảng 10 km của các tỉnh giáp ranh (Đồng Nai, Tây Ninh…). Côn Đảo vẫn bị bỏ vì không có đường bộ.

**Cách lấy dữ liệu.**
1. Tự động: lần khởi động đầu BE tải qua Overpass, chia thành vài chục truy vấn. Máy chủ Overpass hay quá tải (502/504); BE tự thử lại, tải dở thì chạy lại vẫn dùng được phần đã tải (cache trong `data/osmnx_cache/`). Có thể đổi máy chủ bằng `OVERPASS_URL`.
2. Từ file OSM của Geofabrik (nên dùng cho cả thành phố, không phụ thuộc Overpass): xem [BE/README.md](../BE/README.md). Script `scripts/graph_from_pbf.py` dùng cùng bộ lọc đường cho ô tô như OSMnx, mất khoảng 20 phút và cần khoảng 6 GB RAM trống.

**Số liệu đo trên máy dev** (Windows, Python 3.14, MySQL 8):

| | |
|---|---|
| Đồ thị dựng được | 289.456 node, 676.505 cạnh, file `.graphml` 317 MB |
| Sau khi giữ thành phần liên thông mạnh lớn nhất | 276.260 node, 651.918 cạnh |
| Khởi động BE lần đầu (đọc `.graphml`, chép vào MySQL) | khoảng 6,5 phút |
| Khởi động các lần sau (đọc từ MySQL) | khoảng 1 phút |
| RAM của BE | khoảng 3,7 GB |
| Bến Thành → Thủ Dầu Một (29,2 km) | Dijkstra ~0,8 s, duyệt 132 nghìn node; A* ~0,3 s, 27 nghìn node |
| Bến Thành → Vũng Tàu (98 km) | Dijkstra 1,4–2,1 s, 268 nghìn node; A* 1,3–2,5 s, 137–140 nghìn node |
| Benchmark 20 cặp ngẫu nhiên | khoảng 40 giây; trung bình Dijkstra 1,35 s, A* 0,76 s |

Tuyến Bến Thành → Vũng Tàu là ví dụ A* không lợi nhiều: đường thật (98 km) dài gấp khoảng 1,5 lần đường chim bay (64 km) vì phải vòng qua Đồng Nai, nên heuristic Haversine ước lượng thấp xa so với thực tế. A* vẫn duyệt ít hơn một nửa số node, nhưng mỗi bước phải tính thêm Haversine nên thời gian gần bằng Dijkstra. Với tuyến gần như thẳng (Thủ Dầu Một) A* duyệt ít hơn 80%.

**Quay về bản đồ nhỏ** để chạy thử nhanh: đặt `PLACE_NAME=District 1, Ho Chi Minh City, Vietnam` và `GRAPH_BUFFER_KM=0`. Mỗi bản đồ có file cache và dòng trong bảng `maps` riêng, đổi qua lại không phải tải hay nhập lại.

## Cơ sở dữ liệu (MySQL)

Không bắt buộc. Để trống `MYSQL_DATABASE` thì BE chạy bình thường nhưng không lưu gì, FE ẩn phần lịch sử. Khi điền `MYSQL_DATABASE`, BE tự tạo database (utf8mb4) và các bảng lúc khởi động; không cần chạy script SQL.

| Bảng | Nội dung |
|---|---|
| `maps` | Mỗi bản đồ đã tải (tên khu vực hoặc bbox), số node, số cạnh. Có thể lưu nhiều bản đồ, ví dụ cả TP.HCM và Quận 1 |
| `nodes` | Nút giao: `osm_id`, `lat`, `lng`, `street_count` |
| `edges` | Đoạn đường `u → v`: `length` (m), `name`, `highway`, `oneway`, `maxspeed` |
| `route_queries` | Lịch sử tìm đường: tọa độ 2 điểm, thuật toán, độ dài, thời gian chạy, số node đã duyệt |
| `benchmark_runs` | Mỗi lần chạy benchmark: số cặp điểm, seed |
| `benchmark_results` | Kết quả từng cặp điểm × thuật toán của một lần benchmark |

```
maps 1───n nodes 1───n edges (u, v)
maps 1───n route_queries
maps 1───n benchmark_runs 1───n benchmark_results
```

- Thứ tự nạp bản đồ khi khởi động: **MySQL → file `.graphml` → tải từ OSM**. Lần đầu có database, BE chép bản đồ vào MySQL.
- Lỗi kết nối database chỉ ghi log, BE vẫn chạy tiếp (không lưu).
- Test dùng SQLite trong bộ nhớ nên CI không cần MySQL.

Truy vấn mẫu cho phần thực nghiệm (chạy trong MySQL Workbench):

```sql
SELECT algorithm, COUNT(*) AS so_cap, AVG(runtime_ms), AVG(visited_count)
FROM benchmark_results WHERE run_id = 1 GROUP BY algorithm;
```

## API

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/graph/info` | Tên khu vực, số node, số cạnh, khung bao bản đồ, có database hay không |
| GET | `/api/route?algo=dijkstra\|astar&from_lat=&from_lng=&to_lat=&to_lng=` | Đường đi, độ dài, thời gian chạy, số node đã duyệt |
| GET | `/api/compare?from_lat=&from_lng=&to_lat=&to_lng=` | Chạy cả 2 thuật toán để so sánh |
| GET | `/api/history?limit=20` | Lịch sử tìm đường mới nhất (503 nếu chưa cấu hình database) |
| POST | `/api/benchmark?n=50&seed=` | Chạy N cặp điểm ngẫu nhiên, trả về thống kê và từng dòng kết quả; lưu vào database nếu có |

Thời gian chạy là **lần nhanh nhất trong 5 lần chạy** để giảm nhiễu đo. Lần chạy nào đã mất từ 100 ms trở lên (tuyến dài trên bản đồ toàn thành phố) thì ít nhiễu nên không chạy lại.

## Luồng hoạt động

```
Người dùng click 2 điểm trên bản đồ (FE)
        │
        ▼
FE gọi GET /api/route  ───────────►  BE
                                     │ tìm node gần nhất với 2 tọa độ
                                     │ chạy Dijkstra hoặc A* trên đồ thị đường
                                     │ trả về đường đi + số liệu
        ◄───────────────────────────┘
FE vẽ đường đi, node đã duyệt và hiển thị số liệu
```

## Cách chạy

**Backend** (terminal 1):
```bash
cd BE
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

**Frontend** (terminal 2):
```bash
cd FE
npm install
copy .env.example .env
npm run dev
```

## CI/CD (GitHub Actions)

Mỗi lần push lên `main` hoặc tạo Pull Request vào `main`, GitHub tự chạy cả 2 workflow.

| Workflow | Các bước |
|---|---|
| `Backend CI` | Cài Python 3.12 → cài thư viện → `ruff check` → kiểm tra cú pháp → `pytest` |
| `Frontend CI` | Cài Node 20 → `npm ci` → `npm run build` → lưu thư mục `dist` (giữ 7 ngày) |

Xem kết quả ở tab **Actions** trên GitHub. Khi thêm thư viện cho FE, nhớ commit cả `package-lock.json`.

Phần CD (tự động deploy) sẽ thêm khi chọn nơi deploy, ví dụ BE lên Render và FE lên Vercel.

> Trạng thái hiện tại: đã có **bản demo** gồm tìm đường Dijkstra/A\*, so sánh 2 thuật toán, vẽ node đã duyệt, lưu MySQL (bản đồ, lịch sử, benchmark) và tab Benchmark. Việc còn lại xem trong [03-chuc-nang-can-lam.md](03-chuc-nang-can-lam.md).
