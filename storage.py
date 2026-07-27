# Phase 4 — In-memory storage for books (no database yet).

# 4.1 -> 1. Dict keyed by id: O(1) lookup for get / update / delete.
#    Value is a plain dict matching BookResponse fields.
books_db: dict[int, dict] = {}

# 4.1 -> 2. Module-level store: lives while the process runs; cleared on restart.
#    Later this becomes a real DB session / table.

# 4.1 -> 3. Auto-increment id counter (simple unique ints for this lesson).
_next_book_id: int = 1


def generate_book_id() -> int:
    """Return a new unique book id, then bump the counter."""
    global _next_book_id
    book_id = _next_book_id
    _next_book_id += 1
    return book_id
