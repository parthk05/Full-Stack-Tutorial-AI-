# Lesson 02 Phase 2.2 / 4B — MongoDB repository (Motor collection ops).
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from db.mongo.models import doc_to_book_dict
from schemas.book_request import BookCreate, BookUpdate


class MongoBookRepository:
    """Parallel API to MySQLBookRepository, backed by a `books` collection."""

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.books = db.books
        self.counters = db.counters

    async def _next_int_id(self) -> int:
        """
        3B.2 -> Integer `id` strategy (matches Lesson 01 BookResponse).
        Atomically increment a counter document; Mongo still has its own `_id`.
        """
        result = await self.counters.find_one_and_update(
            {"_id": "books"},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return int(result["seq"])

    # 4B.1 -> CREATE
    async def create(self, data: BookCreate) -> dict[str, Any]:
        book_id = await self._next_int_id()
        doc = {"id": book_id, **data.model_dump()}
        await self.books.insert_one(doc)
        return doc_to_book_dict(doc)

    # 4B.2 -> LIST
    async def list(self, skip: int = 0, limit: int = 50) -> list[dict[str, Any]]:
        cursor = self.books.find().skip(skip).limit(limit).sort("id", 1)
        return [doc_to_book_dict(doc) async for doc in cursor]

    async def get(self, book_id: int) -> dict[str, Any] | None:
        doc = await self.books.find_one({"id": book_id})
        return doc_to_book_dict(doc) if doc else None

    async def update(self, book_id: int, data: BookUpdate) -> dict[str, Any] | None:
        updates = data.model_dump(exclude_unset=True)
        if not updates:
            return await self.get(book_id)
        doc = await self.books.find_one_and_update(
            {"id": book_id},
            {"$set": updates},
            return_document=ReturnDocument.AFTER,
        )
        return doc_to_book_dict(doc) if doc else None

    async def delete(self, book_id: int) -> bool:
        result = await self.books.delete_one({"id": book_id})
        return result.deleted_count > 0
