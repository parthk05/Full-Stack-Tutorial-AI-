# Lesson 02 Phase 2.2 / 4A — MySQL repository (SQL only; no HTTP here).
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.mysql.models import Book
from schemas.book_request import BookCreate, BookUpdate


class MySQLBookRepository:
    """Thin data-access layer: create / list / get / update / delete."""

    def __init__(self, db: Session) -> None:
        self.db = db

    # 4A.1 -> CREATE
    def create(self, data: BookCreate) -> Book:
        book = Book(**data.model_dump())
        self.db.add(book)
        self.db.commit()  # persist transaction
        self.db.refresh(book)  # load DB-generated id
        return book

    # 4A.2 -> LIST (+ 5.3 pagination)
    def list(self, skip: int = 0, limit: int = 50) -> list[Book]:
        stmt = select(Book).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    # 4A.3 -> GET by id
    def get(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    # 4A.4 -> UPDATE
    def update(self, book: Book, data: BookUpdate) -> Book:
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(book, key, value)
        self.db.commit()
        self.db.refresh(book)
        return book

    # 4A.5 -> DELETE
    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()
