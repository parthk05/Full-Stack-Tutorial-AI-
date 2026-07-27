# Lesson 02 Phase 1.3 — Typed settings loaded from .env (never hardcode secrets).
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Reads environment variables / .env into typed fields."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- MySQL (3A) ---
    # Prefer a full SQLAlchemy URL, e.g.:
    # mysql+pymysql://user:password@localhost:3306/fastapi_books
    MYSQL_URL: str = "mysql+pymysql://root:password@localhost:3306/fastapi_books"

    # --- MongoDB (3B) ---
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "fastapi_books"

    # --- List pagination caps (Phase 5.3) ---
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100


@lru_cache
def get_settings() -> Settings:
    # Cached so we do not re-read .env on every Depends() call.
    return Settings()
