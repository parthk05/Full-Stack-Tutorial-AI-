# Lesson 02 Phase 3A.2 — SQLAlchemy ORM model for Book (MySQL table).
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


class Book(Base):
    """
    Relational mapping of Lesson 01 Book fields.
    id is AUTO_INCREMENT PK — matches BookResponse.id (int).
    """

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    genre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # 5.2 -> Index on published_year for filtered / sorted queries later
    published_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
