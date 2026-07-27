from fastapi import FastAPI

# 6.4 -> Mount resource routers here; keep main thin.
from routers.books_routes import router as books_router

# 1.1 -> Instantiate the FastAPI application.
app = FastAPI(
    title="Books API",
    description="In-memory CRUD tutorial (no database yet)",
    version="0.1.0",
)

# 6.4 -> Wire APIRouter so /books/* routes are registered on the app.
app.include_router(books_router)


# 1.1 -> Health / welcome route
@app.get("/")
async def root():
    return {"message": "Success, Server is healthy!"}
