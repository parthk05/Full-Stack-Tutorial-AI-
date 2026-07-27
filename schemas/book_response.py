# 3.2 -> Response models returned to the client (always include id).
from typing import List, Optional

from pydantic import BaseModel, Field


class BookResponse(BaseModel):
    id: int
    title: str
    genre: Optional[str] = None
    published_year: int
    price: float
    in_stock: bool


class BookResponseList(BaseModel):
    books: List[BookResponse] = Field(..., description="List of books")
