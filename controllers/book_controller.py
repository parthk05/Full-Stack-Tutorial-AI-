# Phase 5 — Business logic for book CRUD (talks to storage, not HTTP details).
from fastapi import HTTPException, status

from schemas.book_request import BookCreate, BookUpdate
from schemas.book_response import BookResponse, BookResponseList
from storage import books_db, generate_book_id


class BookController:
    """Static methods keep routes thin: validate/HTTP in router, logic here."""

    @staticmethod
    def _get_or_404(book_id: int) -> dict:
        # 6.2 -> Use HTTPException for client errors (not bare Exception).
        book = books_db.get(book_id)
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found",
            )
        return book

    # 5.1 -> CREATE
    @staticmethod
    async def create_book(book: BookCreate) -> BookResponse:
        book_id = generate_book_id()
        # model_dump(): Pydantic model -> plain dict for in-memory store
        stored = {"id": book_id, **book.model_dump()}
        books_db[book_id] = stored
        return BookResponse(**stored)

    # 5.2 -> LIST
    @staticmethod
    async def get_books() -> BookResponseList:
        books = [BookResponse(**item) for item in books_db.values()]
        return BookResponseList(books=books)

    # 5.3 -> READ one
    @staticmethod
    async def get_book(book_id: int) -> BookResponse:
        book = BookController._get_or_404(book_id)
        return BookResponse(**book)

    # 5.4 -> UPDATE (partial: only fields the client sent)
    @staticmethod
    async def update_book(book_id: int, book: BookUpdate) -> BookResponse:
        existing = BookController._get_or_404(book_id)
        # exclude_unset=True: skip fields the client omitted (PATCH-style on PUT)
        updates = book.model_dump(exclude_unset=True)
        existing.update(updates)
        books_db[book_id] = existing
        return BookResponse(**existing)

    # 5.5 -> DELETE
    @staticmethod
    async def delete_book(book_id: int) -> None:
        BookController._get_or_404(book_id)
        del books_db[book_id]
