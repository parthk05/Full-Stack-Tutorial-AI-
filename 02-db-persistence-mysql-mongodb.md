# Lesson 02 — Database Persistence (MySQL + MongoDB)

**Prerequisites:** Finish Lesson 01. Your Books CRUD API should run with in-memory `storage.py`, routers, controllers, and Pydantic schemas.

**Goal:** Replace in-memory storage with real persistence. Implement the **same Books CRUD** twice — once with **MySQL** (relational) and once with **MongoDB** (document) — so you learn both models and when to use each.

**Rules for you:**
- Do each step yourself. Do not skip ahead.
- After each step marked **Check**, verify before continuing.
- Keep Lesson 01 schemas and route shapes as stable as possible; swap the persistence layer underneath.
- Prefer official docs when stuck: FastAPI, SQLAlchemy, Motor / PyMongo, MySQL, MongoDB.
- Best practices appear as *why* questions — answer them in your own notes.

**Suggested docs:**
- FastAPI SQL databases: https://fastapi.tiangolo.com/tutorial/sql-databases/
- FastAPI MongoDB (community patterns via Motor): https://motor.readthedocs.io/
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/

---

## Phase 0 — Mindset & design (before installing anything)

### Step 0.1 — Why leave in-memory?
1. List what breaks with `storage.py` after a server restart.
2. In notes: *What does “persistence” mean for an API?*

### Step 0.2 — Relational vs document (high level)
1. Sketch your `Book` fields from Lesson 01.
2. Draw how they become:
   - a **MySQL table** (columns, types, primary key)
   - a **MongoDB document** (fields, `_id`)
3. In notes: *When would you prefer MySQL? When MongoDB?*

### Step 0.3 — Dual-backend plan for this lesson
Decide one of these project approaches (pick one and stick to it):

| Approach | Idea |
|----------|------|
| A — Side-by-side | Separate routers/prefixes, e.g. `/mysql/books` and `/mongo/books` |
| B — Switchable | One `/books` API; choose backend via env var (`DB_BACKEND=mysql\|mongo`) |
| C — Parallel modules | Shared schemas; `repositories/mysql_book_repo.py` and `repositories/mongo_book_repo.py` |

**Check:** You wrote down which approach you chose and why.

---

## Phase 1 — Environment & secrets

### Step 1.1 — Install databases locally
1. Install **MySQL** (or MariaDB) and confirm you can connect with a client / CLI.
2. Install **MongoDB** and confirm `mongosh` (or Compass) connects.
3. Create an empty MySQL database for this project (e.g. `fastapi_books`).
4. Note MongoDB database name you will use (e.g. `fastapi_books`).

**Check:** Both servers are running; you can connect without the FastAPI app.

### Step 1.2 — Dependencies
1. Extend `requirements.txt` (do not remove FastAPI/Uvicorn).
2. Add packages for:
   - settings / env loading (commonly `python-dotenv` or `pydantic-settings`)
   - MySQL + SQLAlchemy async or sync driver stack (research current recommended combo)
   - MongoDB async driver (commonly Motor) or sync PyMongo — pick one style and stay consistent with how you write FastAPI routes
3. Install from `requirements.txt`.

**Check:** You can import the new libraries in the venv REPL.

### Step 1.3 — Configuration (never hardcode secrets)
1. Create a `.env` file (and ensure it is in `.gitignore`).
2. Put placeholders for:
   - MySQL URL / host, port, user, password, database name
   - MongoDB URI and database name
   - Optional: `DB_BACKEND` if you chose approach B
3. Create a settings module that loads these into typed config.
4. In notes: *Why must DB passwords stay out of git?*

**Check:** App can print “settings loaded” without printing the raw password.

---

## Phase 2 — Project structure for persistence

### Step 2.1 — Folders to add
Extend Lesson 01 structure. Typical layout (adjust names to your taste):

```text
db/
  mysql/
    session.py      # engine + session / dependency
    models.py       # SQLAlchemy table models
  mongo/
    client.py       # client + db handle / dependency
    models.py       # document shape (ODM or plain dict helpers)
repositories/       # optional: CRUD functions per backend
```

### Step 2.2 — Repository idea (best practice)
1. Controllers should not embed raw SQL / collection calls forever.
2. Plan a thin layer: `create_book`, `list_books`, `get_book`, `update_book`, `delete_book` per backend.
3. In notes: *Why separate router → controller → repository → DB?*

**Check:** You know which file will replace calls currently using `books_db` / `generate_book_id`.

---

## Part A — MySQL persistence

> Complete Part A fully (CRUD works against MySQL) before starting Part B, unless you intentionally implement both in parallel.

---

## Phase 3A — MySQL connection & models

### Step 3A.1 — Engine and session
1. Create the SQLAlchemy engine from your settings URL.
2. Create a session factory.
3. Write a FastAPI **dependency** that yields a DB session and closes it after the request.
4. In notes: *What goes wrong if you never close sessions?*

**Check:** A throwaway route (or startup hook) can open a session and run `SELECT 1` successfully.

### Step 3A.2 — ORM model for Book
1. Map Lesson 01 fields to SQLAlchemy columns with sensible SQL types.
2. Define a primary key (`id` autoincrement integer is fine to match Lesson 01 responses).
3. Decide nullability to match your Pydantic create schema.

**Check:** Model imports without errors.

### Step 3A.3 — Create tables
1. Choose one approach for this lesson:
   - **Simple:** `create_all` on startup (OK for learning)
   - **Better:** Alembic migrations (preferred if you want production habits)
2. If using Alembic: init, write first migration, upgrade.
3. In notes: *Why are migrations safer than create_all in real apps?*

**Check:** The `books` (or equivalent) table exists in MySQL.

---

## Phase 4A — MySQL CRUD (replace in-memory)

Do these **in order**. Test each in `/docs`.

### Step 4A.1 — CREATE
1. Accept `BookCreate`.
2. Insert via session; commit; refresh.
3. Return `BookResponse` with DB-generated `id`, status `201`.

**Check:** Row appears in MySQL; restart server; book still exists.

### Step 4A.2 — LIST
1. Query all books (add `limit`/`offset` later if you want).
2. Empty list is valid.

### Step 4A.3 — GET by id
1. Lookup by primary key.
2. `404` if missing.

### Step 4A.4 — UPDATE
1. Load existing; apply update schema fields; commit.
2. `404` if missing.

### Step 4A.5 — DELETE
1. Delete row; return `204` (or your Lesson 01 convention).
2. `404` if missing.

**Check:** Full CRUD works; data survives restart; unknown ids return 404.

### Step 4A.6 — Wire dependency injection
1. Routes/controllers receive the DB session via `Depends(...)`.
2. Remove (or stop using) MySQL paths that still touch `storage.books_db`.
3. In notes: *How does `Depends` help testing later?*

---

## Part B — MongoDB persistence

---

## Phase 3B — Mongo connection & document design

### Step 3B.1 — Client lifecycle
1. Create a Mongo client from your URI (prefer app lifespan / startup-shutdown hooks).
2. Expose the database (and `books` collection) via a dependency or module accessor.
3. In notes: *Why connect once at startup instead of per request?*

**Check:** You can `ping` the server or list collection names from a tiny probe.

### Step 3B.2 — Document shape vs `_id`
1. Decide how API `id` relates to Mongo `_id`:
   - expose ObjectId as string in responses, **or**
   - store an integer `id` field in addition to `_id`
2. Write down the tradeoff (Lesson 01 used integer ids).
3. Update response thinking: clients must still get a stable identifier.

**Check:** You documented the id strategy before coding CRUD.

### Step 3B.3 — Optional ODM
1. Either use plain Motor collection operations, or an ODM (e.g. Beanie) — pick one.
2. Keep Pydantic request/response schemas as the API contract either way.

---

## Phase 4B — MongoDB CRUD

### Step 4B.1 — CREATE
1. Insert document from `BookCreate`.
2. Return response with your chosen id representation, status `201`.

**Check:** Document visible in Compass / `mongosh`; survives restart.

### Step 4B.2 — LIST / GET / UPDATE / DELETE
1. Implement the same four operations as MySQL.
2. Mirror status codes and 404 behavior from Lesson 01 / Part A.
3. For update: only set fields the client sent (same idea as `exclude_unset`).

**Check:** `/mongo/books` (or your chosen paths) fully CRUD against MongoDB.

### Step 4B.3 — Align controllers
1. MySQL and Mongo repositories should feel parallel (same method names if possible).
2. Controllers call repositories; routers stay thin.

---

## Phase 5 — Cross-cutting best practices (both DBs)

### Step 5.1 — Errors & transactions mindset
1. Map DB “not found” to HTTP 404 consistently.
2. For MySQL writes: know when you need `commit` / `rollback`.
3. For Mongo: know what a failed insert looks like and how you surface it.
4. In notes: *What is a transaction? Does your Mongo lesson use multi-doc transactions?*

### Step 5.2 — Indexes (intro)
1. Add an index useful for your queries (e.g. unique title, or `published_year`) on **each** backend.
2. In notes: *What problem do indexes solve? What do they cost?*

### Step 5.3 — Pagination (intro)
1. Add `skip`/`limit` or `page`/`size` query params to list endpoints (both backends if time allows).
2. Cap max page size so clients cannot request unbounded lists.

### Step 5.4 — Health checks
1. Add `/health` (or extend `/`) to report MySQL and Mongo connectivity separately.
2. Do not leak credentials in the response.

### Step 5.5 — Cleanup Lesson 01 storage
1. Once both backends work, mark `storage.py` deprecated or delete usages.
2. Ensure no production path still writes only to the in-memory dict.

---

## Phase 6 — Compare & choose (learning outcome)

### Step 6.1 — Same API, two stores
Fill this table in your notes after both backends work:

| Concern | MySQL | MongoDB |
|---------|-------|---------|
| Schema rigidity | | |
| Id type | | |
| Migrations / evolution | | |
| Query style | | |
| Good fit for Books? | | |

### Step 6.2 — When not to use both
1. In notes: *Why would a real product usually pick one primary DB for a resource?*
2. Dual-write (MySQL + Mongo for the same book) is out of scope unless you intentionally study consistency problems.

---

## Phase 7 — Self-review checklist

Before you call Lesson 02 done, confirm:

- [ ] `.env` exists locally and is gitignored; settings load cleanly
- [ ] MySQL Books CRUD works and survives restart
- [ ] MongoDB Books CRUD works and survives restart
- [ ] DB sessions/clients use FastAPI dependencies or lifespan correctly
- [ ] 404 / 201 / 204 behavior matches Lesson 01 conventions
- [ ] Controllers no longer depend on in-memory `books_db` for the DB routes
- [ ] You can explain: engine/session vs Mongo client/collection, ORM model vs document, migrations vs `create_all`, repository pattern
- [ ] You wrote short notes comparing MySQL vs Mongo for this API

---

## What to do next (do not start until Lesson 02 is done)

Lesson 03: authentication & authorization — sessions, JWT, and OAuth — protecting these persisted APIs.

---

## How to use this file

1. Complete one step.
2. Mark it done in this file or in your notes.
3. If stuck for more than ~20 minutes, re-read the matching docs section, then ask for a **hint** (not the full solution) for that step only.
4. Prefer finishing **Part A (MySQL)** end-to-end before deep-diving Part B, so you always have one working persistence path.
