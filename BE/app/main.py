# Điểm khởi chạy FastAPI: tạo app, bật CORS, gắn router /api
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings
from app.graph_loader import graph_info, load_graph

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Nạp đồ thị một lần khi khởi động, mọi request dùng chung
    app.state.graph = None
    app.state.graph_info = None
    try:
        app.state.graph = load_graph(settings.place_name, settings.graph_cache_file)
        app.state.graph_info = graph_info(app.state.graph, settings.place_name)
    except NotImplementedError:
        # Khi graph_loader chưa xong, server vẫn chạy để FE thử /health; API bản đồ trả 503
        logger.warning("graph_loader chưa được cài đặt, chưa có bản đồ")
    yield


app = FastAPI(title="Digital Map Pathfinding API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
