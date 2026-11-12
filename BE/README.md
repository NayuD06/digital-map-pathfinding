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

Kiểm tra: http://localhost:8000/health trả về `{"status": "ok"}`.

Chạy test và kiểm tra code giống CI:

```bash
pip install ruff
ruff check .
pytest
```

Định dạng API: [docs/05-dinh-dang-api.md](../docs/05-dinh-dang-api.md).
