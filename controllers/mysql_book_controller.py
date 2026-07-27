# Lesson 02 Part A — MySQL book controller (HTTP errors + repo orchestration).
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.mysql.models import Book
from repositories.mysql_book_repo import MySQLBookRepository
from schemas.book_request import BookCreate, BookUpdate
from schemas.book_response import BookResponse, BookResponseList


def _to_response(book: Book) -> BookResponse:
    return BookResponse(
        id=book.id,
        title=book.title,
        genre=book.genre,
        published_year=book.published_year,
        price=book.price,
        in_stock=book.in_stock,
    )


class MySQLBookController:
    """Router → controller → repository → MySQL."""

    @staticmethod
    def _get_or_404(db: Session, book_id: int) -> Book:
        # 5.1 -> Map "not found" to HTTP 404 (not a bare Exception).
        book = MySQLBookRepository(db).get(book_id)
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found",
            )
        return book

    @staticmethod
    async def create_book(db: Session, book: BookCreate) -> BookResponse:
        created = MySQLBookRepository(db).create(book)
        return _to_response(created)

    @staticmethod
    async def get_books(db: Session, skip: int, limit: int) -> BookResponseList:
        books = MySQLBookRepository(db).list(skip=skip, limit=limit)
        return BookResponseList(books=[_to_response(b) for b in books])

    @staticmethod
    async def get_book(db: Session, book_id: int) -> BookResponse:
        return _to_response(MySQLBookController._get_or_404(db, book_id))

    @staticmethod
    async def update_book(
        db: Session, book_id: int, book: BookUpdate
    ) -> BookResponse:
        existing = MySQLBookController._get_or_404(db, book_id)
        updated = MySQLBookRepository(db).update(existing, book)
        return _to_response(updated)

    @staticmethod
    async def delete_book(db: Session, book_id: int) -> None:
        existing = MySQLBookController._get_or_404(db, book_id)
        MySQLBookRepository(db).delete(existing)
