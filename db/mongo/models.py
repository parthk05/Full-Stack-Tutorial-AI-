# Lesson 02 Phase 3B.2 — Document helpers (plain Motor dicts, no ODM).
# API still exposes integer `id` (Lesson 01 compatible).
# Mongo also keeps its own `_id` (ObjectId); we store a parallel int `id` field.

from typing import Any


def doc_to_book_dict(doc: dict[str, Any]) -> dict[str, Any]:
    """Strip Mongo `_id`; keep public fields used by BookResponse."""
    return {
        "id": doc["id"],
        "title": doc["title"],
        "genre": doc.get("genre"),
        "published_year": doc["published_year"],
        "price": doc["price"],
        "in_stock": doc["in_stock"],
    }
