# Lesson 02 Phase 3A.1 — MySQL engine, session factory, and FastAPI Depends.
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from core.settings import get_settings
from db.mysql.models import Base

settings = get_settings()

# Engine: one per process; manages the connection pool to MySQL.
engine = create_engine(
    settings.MYSQL_URL,
    pool_pre_ping=True,  # drop stale connections before use
)

# Session factory: each request gets its own Session.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_mysql() -> None:
    """
    3A.3 -> Simple create_all for learning (Alembic is safer in production).
    Creates tables if they do not exist; does not alter existing columns.
    """
    Base.metadata.create_all(bind=engine)


def get_mysql_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency: yield a session, always close afterward.
    Never closing sessions leaks connections from the pool.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def mysql_ping() -> bool:
    """Phase 5.4 — health check helper (no credentials in response)."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
