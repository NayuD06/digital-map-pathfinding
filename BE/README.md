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

- Mặc định dùng bản đồ **toàn TP.HCM theo ranh giới mới** (`PLACE_NAME=Ho Chi Minh City, Vietnam`), nới thêm 10 km sang tỉnh lân cận (`GRAPH_BUFFER_KM=10`) vì đường ra Vũng Tàu đi qua Đồng Nai. Lần chạy đầu BE tải bản đồ từ OpenStreetMap rồi lưu vào `data/ho-chi-minh-city-vietnam-10-km.graphml`; tải dở bị lỗi thì chạy lại, phần đã tải nằm trong `data/osmnx_cache/` nên không tải lại từ đầu.
- Muốn chạy nhanh với một quận: đặt `PLACE_NAME=District 1, Ho Chi Minh City, Vietnam` và `GRAPH_BUFFER_KM=0`. Mỗi bản đồ có file cache riêng nên đổi qua lại không cần xóa file.
- `overpass-api.de` quá tải (log báo 502/504 hoặc timeout) thì đặt `OVERPASS_URL=https://maps.mail.ru/osm/tools/overpass/api` trong `.env`.
- Overpass không tải nổi cả thành phố thì dựng bản đồ từ file OSM của Geofabrik (khoảng 330 MB, cập nhật hằng ngày):
  ```bash
  pip install osmium
  python -m scripts.graph_from_pbf duong/dan/vietnam-latest.osm.pbf
  ```
  File tải ở https://download.geofabrik.de/asia/vietnam-latest.osm.pbf. Script dùng cùng bộ lọc đường cho ô tô như OSMnx và ghi ra file cache của bản đồ trong `.env` (mất khoảng 20 phút, cần khoảng 6 GB RAM trống), sau đó khởi động BE như bình thường. Lần khởi động đầu chép bản đồ vào MySQL mất khoảng 6,5 phút, các lần sau khoảng 1 phút.
- Chạy test: `pytest`. Test trên bản đồ thật chỉ chạy khi đã có file cache, vì vậy trên CI test này bị bỏ qua.
- Kiểm tra code: `ruff check .`

## Lưu dữ liệu vào MySQL

1. Mở `.env`, điền `MYSQL_PASSWORD` và đặt tên database, ví dụ `MYSQL_DATABASE=digital_map`.
2. Khởi động lại BE. Log hiện `Đã kết nối database ...` và `Đã lưu bản đồ vào database` là được.

BE tự tạo database và các bảng, không cần chạy script SQL. Mô tả các bảng xem trong [docs/01-cau-truc-du-an.md](../docs/01-cau-truc-du-an.md#cơ-sở-dữ-liệu-mysql).

Muốn dùng database khác, đặt `DATABASE_URL` theo cú pháp SQLAlchemy (ví dụ `sqlite:///data/dev.db`); biến này được ưu tiên hơn các biến `MYSQL_*`.
