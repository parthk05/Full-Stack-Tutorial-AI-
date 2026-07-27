# Lesson 02 Phase 3B.1 — Mongo client lifecycle (one client for the process).
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from core.settings import get_settings

_client: AsyncIOMotorClient | None = None


async def connect_mongo() -> None:
    """Call on app startup — connect once, reuse across requests."""
    global _client
    settings = get_settings()
    _client = AsyncIOMotorClient(settings.MONGODB_URI)
    # Force a server round-trip so bad URIs fail fast at startup.
    await _client.admin.command("ping")
    db = _client[settings.MONGODB_DATABASE]
    # 5.2 -> Indexes: faster lookups / filters; cost = write overhead + disk
    await db.books.create_index("id", unique=True)
    await db.books.create_index("published_year")
    await db.books.create_index("title")


async def close_mongo() -> None:
    """Call on app shutdown — release sockets cleanly."""
    global _client
    if _client is not None:
        _client.close()
        _client = None


def get_mongo_db() -> AsyncIOMotorDatabase:
    """Dependency / accessor for the configured database."""
    if _client is None:
        raise RuntimeError("MongoDB client is not connected. Check lifespan startup.")
    settings = get_settings()
    return _client[settings.MONGODB_DATABASE]


async def mongo_ping() -> bool:
    """Phase 5.4 — health check helper."""
    try:
        if _client is None:
            return False
        await _client.admin.command("ping")
        return True
    except Exception:
        return False
