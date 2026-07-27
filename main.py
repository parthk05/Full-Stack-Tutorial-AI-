# Lesson 02 — App entry: lifespan (DB connect), dual routers, health checks.
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.settings import get_settings
from db.mongo.client import close_mongo, connect_mongo, mongo_ping
from db.mysql.session import init_mysql, mysql_ping
from routers.mongo_books_routes import router as mongo_books_router
from routers.mysql_books_routes import router as mysql_books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    3A.3 / 3B.1 -> Startup: MySQL create_all + Mongo connect/indexes.
    Shutdown: close Mongo client.
    MySQL engine lives for the process; sessions are per-request via Depends.
    """
    # Settings load once (and confirm .env is readable without printing secrets).
    get_settings()
    init_mysql()
    await connect_mongo()
    yield
    await close_mongo()


app = FastAPI(
    title="Books API",
    description=(
        "Lesson 02 — Books CRUD with MySQL and MongoDB side-by-side. "
        "Use /mysql/books and /mongo/books (in-memory storage removed)."
    ),
    version="0.2.0",
    lifespan=lifespan,
)

# Approach A — separate prefixes so both backends coexist for learning.
app.include_router(mysql_books_router)
app.include_router(mongo_books_router)


@app.get("/")
async def root():
    return {
        "message": "Success, Server is healthy!",
        "docs": "/docs",
        "mysql_books": "/mysql/books",
        "mongo_books": "/mongo/books",
        "health": "/health",
    }


# 5.4 -> Health: report connectivity only (never leak credentials).
@app.get("/health")
async def health():
    return {
        "mysql": "up" if mysql_ping() else "down",
        "mongodb": "up" if await mongo_ping() else "down",
    }
