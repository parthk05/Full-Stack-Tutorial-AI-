# 3.1 -> Request bodies for create / update (no client-supplied id on create).
from typing import Optional

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    genre: Optional[str] = None
    published_year: int = Field(..., gt=1900, lt=2026)
    price: float = Field(..., gt=0)
    in_stock: bool = Field(default=True)


# 3.3 -> PATCH-style update: all fields optional; omit = leave unchanged.
class BookUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    published_year: Optional[int] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None
