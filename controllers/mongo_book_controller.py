# Lesson 02 Part B — MongoDB book controller.
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from repositories.mongo_book_repo import MongoBookRepository
from schemas.book_request import BookCreate, BookUpdate
from schemas.book_response import BookResponse, BookResponseList


class MongoBookController:
    """Router → controller → repository → MongoDB."""

    @staticmethod
    async def create_book(db: AsyncIOMotorDatabase, book: BookCreate) -> BookResponse:
        created = await MongoBookRepository(db).create(book)
        return BookResponse(**created)

    @staticmethod
    async def get_books(
        db: AsyncIOMotorDatabase, skip: int, limit: int
    ) -> BookResponseList:
        books = await MongoBookRepository(db).list(skip=skip, limit=limit)
        return BookResponseList(books=[BookResponse(**b) for b in books])

    @staticmethod
    async def get_book(db: AsyncIOMotorDatabase, book_id: int) -> BookResponse:
        book = await MongoBookRepository(db).get(book_id)
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found",
            )
        return BookResponse(**book)

    @staticmethod
    async def update_book(
        db: AsyncIOMotorDatabase, book_id: int, book: BookUpdate
    ) -> BookResponse:
        updated = await MongoBookRepository(db).update(book_id, book)
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found",
            )
        return BookResponse(**updated)

    @staticmethod
    async def delete_book(db: AsyncIOMotorDatabase, book_id: int) -> None:
        deleted = await MongoBookRepository(db).delete(book_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found",
            )
