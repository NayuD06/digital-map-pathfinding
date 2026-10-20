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
