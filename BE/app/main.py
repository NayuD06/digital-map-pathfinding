# Điểm khởi chạy FastAPI: tạo app, bật CORS, gắn router /api
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings
from app.db import create_session_factory
from app.graph_loader import graph_info, load_graph

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kết nối database (nếu có) và nạp đồ thị một lần khi khởi động, các request dùng chung
    app.state.db = create_session_factory(settings.db_url)
    app.state.graph, app.state.map_id = load_graph(app.state.db)
    app.state.graph_info = {**graph_info(app.state.graph), "database_enabled": app.state.db is not None}
    yield


app = FastAPI(title="Digital Map Pathfinding API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
