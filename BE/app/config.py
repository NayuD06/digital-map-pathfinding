# Đọc cấu hình từ .env: PORT, PLACE_NAME, CORS_ORIGINS, GRAPH_CACHE_PATH, GRAPH_BBOX, MYSQL_*
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, make_url

# Thư mục BE/, để đường dẫn tương đối không phụ thuộc nơi chạy lệnh
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    port: int = 8000
    place_name: str = "District 1, Ho Chi Minh City, Vietnam"
    # Nhiều origin cách nhau bằng dấu phẩy
    cors_origins: str = "http://localhost:5173"
    graph_cache_path: str = "data/graph.graphml"
    # Phương án dự phòng khi không tìm được ranh giới theo tên: "west,south,east,north"
    graph_bbox: str = ""

    # MySQL: điền MYSQL_DATABASE để bật lưu dữ liệu, để trống thì chạy không cần database
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = ""
    mysql_database: str = ""
    # Ghi đè toàn bộ chuỗi kết nối nếu cần, ví dụ sqlite:///data/dev.db
    database_url: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def graph_cache_file(self) -> Path:
        path = Path(self.graph_cache_path)
        return path if path.is_absolute() else BASE_DIR / path

    @property
    def map_name(self) -> str:
        """Tên dùng để nhận ra bản đồ trong database."""
        return f"bbox:{self.graph_bbox}" if self.graph_bbox else self.place_name

    @property
    def db_url(self) -> URL | None:
        if self.database_url:
            return make_url(self.database_url)
        if self.mysql_database:
            # URL.create tự xử lý ký tự đặc biệt trong mật khẩu như @, #, /
            return URL.create(
                "mysql+pymysql",
                username=self.mysql_user,
                password=self.mysql_password,
                host=self.mysql_host,
                port=self.mysql_port,
                database=self.mysql_database,
                query={"charset": "utf8mb4"},
            )
        return None


settings = Settings()
