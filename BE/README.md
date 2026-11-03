# Backend – FastAPI + OSMnx

Chạy ở port **8000**.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Tài liệu API: http://localhost:8000/docs

- Lần chạy đầu sẽ tải bản đồ Quận 1 từ OpenStreetMap, mất khoảng vài chục giây, rồi lưu cache vào `data/graph.graphml`. Đổi `PLACE_NAME` thì xóa file này để tải lại.
- Chạy test: `pytest`. Test trên bản đồ thật chỉ chạy khi đã có file cache, vì vậy trên CI test này bị bỏ qua.
- Kiểm tra code: `ruff check .`

## Lưu dữ liệu vào MySQL

1. Mở `.env`, điền `MYSQL_PASSWORD` và đặt tên database, ví dụ `MYSQL_DATABASE=digital_map`.
2. Khởi động lại BE. Log hiện `Đã kết nối database ...` và `Đã lưu bản đồ vào database` là được.

BE tự tạo database và các bảng, không cần chạy script SQL. Mô tả các bảng xem trong [docs/01-cau-truc-du-an.md](../docs/01-cau-truc-du-an.md#cơ-sở-dữ-liệu-mysql).

Muốn dùng database khác, đặt `DATABASE_URL` theo cú pháp SQLAlchemy (ví dụ `sqlite:///data/dev.db`); biến này được ưu tiên hơn các biến `MYSQL_*`.
