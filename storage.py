# DEPRECATED (Lesson 02 Phase 5.5) — In-memory store from Lesson 01.
# Books CRUD now uses MySQL (/mysql/books) and MongoDB (/mongo/books).
# Kept only as a reference; do not import this in production paths.

books_db: dict[int, dict] = {}
_next_book_id: int = 1


def generate_book_id() -> int:
    global _next_book_id
    book_id = _next_book_id
    _next_book_id += 1
    return book_id
