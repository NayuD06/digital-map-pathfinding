# Cấu trúc dự án

Dự án gồm 2 phần chạy **độc lập, mỗi phần một port**:

| Phần | Thư mục | Công nghệ | Port |
|---|---|---|---|
| Backend | `BE/` | Python 3.12, FastAPI, OSMnx, NetworkX | 8000 |
| Frontend | `FE/` | React 18, Vite, Leaflet, Recharts | 5173 |

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
│   │   ├── graph_loader.py       # Tải bản đồ quận bằng OSMnx, cache .graphml
│   │   ├── schemas.py            # Pydantic models cho request/response
│   │   ├── api/
│   │   │   └── routes.py         # Các endpoint /api/...
│   │   └── algorithms/
│   │       ├── dijkstra.py       # Thuật toán Dijkstra (tự cài đặt)
│   │       ├── astar.py          # Thuật toán A* (heuristic Haversine)
│   │       └── utils.py          # Haversine, dựng lại đường đi, tìm node gần nhất
│   ├── data/                     # Nơi lưu file bản đồ cache (không push lên git)
│   └── tests/
│       └── test_algorithms.py    # Kiểm thử thuật toán bằng pytest
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
        ├── api/
        │   └── client.js         # Hàm gọi API backend
        └── components/
            ├── MapView.jsx       # Bản đồ Leaflet, chọn điểm, vẽ đường đi
            ├── ControlPanel.jsx  # Chọn thuật toán, nút Tìm đường / So sánh
            ├── StatsPanel.jsx    # Độ dài, thời gian chạy, số node đã duyệt
            └── CompareChart.jsx  # Biểu đồ so sánh hiệu năng
```

## Cấu hình môi trường

**`BE/.env`**
```
PORT=8000
PLACE_NAME=District 1, Ho Chi Minh City, Vietnam
CORS_ORIGINS=http://localhost:5173
GRAPH_CACHE_PATH=data/graph.graphml
```

**`FE/.env`**
```
VITE_API_URL=http://localhost:8000
```

File `.env` thật không được đưa lên git, chỉ có `.env.example`.

## API dự kiến

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/graph/info` | Tên quận, số node, số cạnh, khung bao bản đồ |
| GET | `/api/route?algo=dijkstra\|astar&from_lat=&from_lng=&to_lat=&to_lng=` | Đường đi, độ dài, thời gian chạy, số node đã duyệt |
| GET | `/api/compare?from_lat=&from_lng=&to_lat=&to_lng=` | Chạy cả 2 thuật toán để so sánh |

## Luồng hoạt động

```
Người dùng click 2 điểm trên bản đồ (FE)
        │
        ▼
FE gọi GET /api/route  ───────────►  BE
                                     │ tìm node gần nhất với 2 tọa độ
                                     │ chạy Dijkstra hoặc A* trên đồ thị quận
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

> Trạng thái hiện tại: mới có **khung thư mục**. Các file code chỉ chứa chú thích mô tả, chưa có logic.
