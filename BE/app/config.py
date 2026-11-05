# Đọc cấu hình từ .env: PORT, PLACE_NAME, CORS_ORIGINS, GRAPH_BUFFER_KM, GRAPH_CACHE_PATH, GRAPH_BBOX, MYSQL_*
import re
import unicodedata
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, make_url

# Thư mục BE/, để đường dẫn tương đối không phụ thuộc nơi chạy lệnh
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    port: int = 8000
    # Toàn TP.HCM theo ranh giới mới (gồm cả Bình Dương, Bà Rịa - Vũng Tàu cũ)
    place_name: str = "Ho Chi Minh City, Vietnam"
    # Nhiều origin cách nhau bằng dấu phẩy
    cors_origins: str = "http://localhost:5173"
    # Để trống thì mỗi bản đồ một file data/<tên bản đồ>.graphml
    graph_cache_path: str = ""
    # Nới ranh giới thêm N km để đường đi được qua tỉnh lân cận: từ trung tâm TP.HCM ra Vũng Tàu
    # phải đi qua Đồng Nai (Long Thành, Nhơn Trạch). Chạy thử với một quận thì đặt 0.
    graph_buffer_km: float = 10
    # Phương án dự phòng khi không tìm được ranh giới theo tên: "west,south,east,north"
    graph_bbox: str = ""
    # Máy chủ Overpass để tải bản đồ, để trống thì dùng mặc định của OSMnx (overpass-api.de)
    overpass_url: str = ""

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
        if self.graph_cache_path:
            path = Path(self.graph_cache_path)
            return path if path.is_absolute() else BASE_DIR / path
        # "Ho Chi Minh City, Vietnam (+10 km)" -> data/ho-chi-minh-city-vietnam-10-km.graphml
        ascii_name = unicodedata.normalize("NFKD", self.map_name).encode("ascii", "ignore").decode()
        slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
        return BASE_DIR / "data" / f"{slug}.graphml"

    @property
    def map_name(self) -> str:
        """Tên dùng để nhận ra bản đồ trong database."""
        if self.graph_bbox:
            return f"bbox:{self.graph_bbox}"
        if self.graph_buffer_km:
            return f"{self.place_name} (+{self.graph_buffer_km:g} km)"
        return self.place_name

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
