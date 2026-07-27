
#APIRouter :- APIRouter is a class that allows you to group related routes together.
#status :- status is a class that allows you to set the status code of the response.
#HTTPException :- HTTPException is a class that allows you to raise an exception and return a response with the exception message.
# Phase 5 + 6 — HTTP routes only; business logic lives in BookController.
# APIRouter groups related routes; status sets response status codes.
from fastapi import APIRouter, status

from controllers.book_controller import BookController
from schemas.book_request import BookCreate, BookUpdate
from schemas.book_response import BookResponse, BookResponseList

#router is an instance of APIRouter class
#prefix is the prefix of the route
#tags is the tags of the route
# 6.4 -> APIRouter groups /books routes; main.py mounts this with include_router.
router = APIRouter(
    prefix="/books",
    tags=["books"],
)
# @router.get:- is a decorator that allows you to define a route for the GET method.
# @router.post:- is a decorator that allows you to define a route for the POST method.
# @router.put:- is a decorator that allows you to define a route for the PUT method.
# @router.delete:- is a decorator that allows you to define a route for the DELETE method.

# status_code :- different status codes are available in the status module

# response_model:- is the model of the response.
# status_code:- is the status code of the response.

# 5.1 -> CREATE — 201 Created + response_model for OpenAPI consistency
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(book: BookCreate) -> BookResponse:
    return await BookController.create_book(book)


# 5.2 -> LIST — empty list is valid (200)
@router.get(
    "/",
    response_model=BookResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_books() -> BookResponseList:
    return await BookController.get_books()


# 5.3 -> READ one — path param book_id; 404 raised in controller
@router.get(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
)
async def get_book(book_id: int) -> BookResponse:
    return await BookController.get_book(book_id)


# 5.4 -> UPDATE — BookUpdate fields optional; only sent fields change
@router.put(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
)
async def update_book(book_id: int, book: BookUpdate) -> BookResponse:
    return await BookController.update_book(book_id, book)


# 5.5 / 6.1 -> DELETE — 204 No Content (no response body)
@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book(book_id: int) -> None:
    await BookController.delete_book(book_id)
