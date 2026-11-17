# Đọc cấu hình từ .env: PORT, PLACE_NAME, CORS_ORIGINS, GRAPH_CACHE_PATH
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Thư mục BE/, để đường dẫn tương đối không phụ thuộc nơi chạy lệnh
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    port: int = 8000
    place_name: str = "District 1, Ho Chi Minh City, Vietnam"
    # Nhiều origin cách nhau bằng dấu phẩy, ví dụ "http://localhost:5173,http://127.0.0.1:5173"
    cors_origins: str = "http://localhost:5173"
    # Đường dẫn tương đối tính từ thư mục BE/
    graph_cache_path: str = "data/graph.graphml"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def graph_cache_file(self) -> Path:
        path = Path(self.graph_cache_path)
        return path if path.is_absolute() else BASE_DIR / path


settings = Settings()
