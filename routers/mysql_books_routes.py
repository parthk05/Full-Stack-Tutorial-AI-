# Lesson 02 Part A — MySQL Books routes: /mysql/books
# Approach A (side-by-side) + Approach C (repository modules).
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from controllers.mysql_book_controller import MySQLBookController
from core.settings import get_settings
from db.mysql.session import get_mysql_session
from schemas.book_request import BookCreate, BookUpdate
from schemas.book_response import BookResponse, BookResponseList

router = APIRouter(
    prefix="/mysql/books",
    tags=["mysql-books"],
)


def _page_limit(limit: int | None = None) -> int:
    """5.3 -> Cap page size so clients cannot request unbounded lists."""
    settings = get_settings()
    size = settings.DEFAULT_PAGE_SIZE if limit is None else limit
    return min(max(size, 1), settings.MAX_PAGE_SIZE)


# 4A.1 -> CREATE
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    book: BookCreate,
    db: Session = Depends(get_mysql_session),  # 4A.6 -> inject session per request
) -> BookResponse:
    return await MySQLBookController.create_book(db, book)


# 4A.2 -> LIST
@router.get(
    "/",
    response_model=BookResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_books(
    skip: int = Query(0, ge=0, description="Number of rows to skip"),
    limit: int = Query(50, ge=1, description="Page size (capped by MAX_PAGE_SIZE)"),
    db: Session = Depends(get_mysql_session),
) -> BookResponseList:
    return await MySQLBookController.get_books(db, skip=skip, limit=_page_limit(limit))


# 4A.3 -> GET one
@router.get(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
)
async def get_book(
    book_id: int,
    db: Session = Depends(get_mysql_session),
) -> BookResponse:
    return await MySQLBookController.get_book(db, book_id)


# 4A.4 -> UPDATE
@router.put(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
)
async def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_mysql_session),
) -> BookResponse:
    return await MySQLBookController.update_book(db, book_id, book)


# 4A.5 -> DELETE
@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book(
    book_id: int,
    db: Session = Depends(get_mysql_session),
) -> None:
    await MySQLBookController.delete_book(db, book_id)
