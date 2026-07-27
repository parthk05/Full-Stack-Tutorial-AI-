# Lesson 02 Part B — MongoDB Books routes: /mongo/books
from fastapi import APIRouter, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers.mongo_book_controller import MongoBookController
from core.settings import get_settings
from db.mongo.client import get_mongo_db
from schemas.book_request import BookCreate, BookUpdate
from schemas.book_response import BookResponse, BookResponseList

router = APIRouter(
    prefix="/mongo/books",
    tags=["mongo-books"],
)


def _page_limit(limit: int) -> int:
    settings = get_settings()
    return min(max(limit, 1), settings.MAX_PAGE_SIZE)


# 4B.1 -> CREATE
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    book: BookCreate,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> BookResponse:
    return await MongoBookController.create_book(db, book)


# 4B.2 -> LIST / GET / UPDATE / DELETE
@router.get(
    "/",
    response_model=BookResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> BookResponseList:
    return await MongoBookController.get_books(db, skip=skip, limit=_page_limit(limit))


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
)
async def get_book(
    book_id: int,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> BookResponse:
    return await MongoBookController.get_book(db, book_id)


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
)
async def update_book(
    book_id: int,
    book: BookUpdate,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> BookResponse:
    return await MongoBookController.update_book(db, book_id, book)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book(
    book_id: int,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> None:
    await MongoBookController.delete_book(db, book_id)
