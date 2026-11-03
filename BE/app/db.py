# Kết nối database bằng SQLAlchemy (MySQL khi chạy thật, SQLite khi test)
import logging

from sqlalchemy import URL, create_engine, make_url, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


def _create_mysql_database(url: URL) -> None:
    """Tạo database nếu chưa có, để không phải vào MySQL tạo tay."""
    # URL.set(database=None) giữ nguyên tên database, nên dùng _replace để bỏ hẳn
    server = create_engine(url._replace(database=None))
    with server.connect() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{url.database}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
    server.dispose()


def create_session_factory(url: URL | str | None) -> sessionmaker | None:
    """Kết nối database và tạo bảng còn thiếu. Không cấu hình hoặc lỗi kết nối thì trả về None."""
    if not url:
        return None
    url = make_url(url)
    # Import để các model đăng ký bảng vào Base.metadata
    from app import models  # noqa: F401

    try:
        if url.get_backend_name() == "mysql":
            _create_mysql_database(url)
        engine = create_engine(url, pool_pre_ping=True)
        Base.metadata.create_all(engine)
    except SQLAlchemyError as e:
        logger.error("Không kết nối được database %s, chạy tiếp không lưu dữ liệu: %s", url, e)
        return None

    logger.info("Đã kết nối database %s", url)
    return sessionmaker(engine, expire_on_commit=False)
