# Lesson 03 — Authentication & Authorization (Sessions, JWT, OAuth)

**Prerequisites:** Finish Lessons 01 and 02. You should have Books CRUD persisted (MySQL and/or MongoDB). You will protect those APIs — do not go back to in-memory-only for this lesson.

**Goal:** Learn the difference between **authentication** (who are you?) and **authorization** (what may you do?), then implement three common mechanisms against your existing FastAPI app:

1. **Session-based** auth (cookie + server-side session)
2. **JWT** (Bearer token, typically stateless)
3. **OAuth 2.0** (login with an external provider; use tokens to call your API)

**Rules for you:**
- Do each step yourself. Do not skip ahead.
- After each step marked **Check**, verify before continuing.
- Implement **one mechanism fully** before starting the next (recommended order below).
- Never commit secrets, client secrets, or private keys.
- Prefer official docs: FastAPI Security, OAuth2, Starlette SessionMiddleware, Authlib / python-jose / PyJWT (pick libraries deliberately).

**Suggested docs:**
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- OAuth2 with Password (and JWT): https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- OAuth2 scopes: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/

---

## Phase 0 — Concepts first (no code yet)

### Step 0.1 — AuthN vs AuthZ
1. Write one sentence each for authentication and authorization.
2. For your Books API, list examples:
   - actions that need only “logged in”
   - actions that need a role (e.g. only `admin` may delete)

### Step 0.2 — Compare the three mechanisms
Fill this before coding:

| | Session cookie | JWT Bearer | OAuth (external IdP) |
|--|----------------|------------|----------------------|
| Where is login state stored? | | | |
| Typical client | Browser / same-site | SPA / mobile / API clients | Browser redirect + API |
| Revocation difficulty | | | |
| CSRF risk? | | | |

### Step 0.3 — Threat basics
1. In notes: password hashing (why never store plaintext), HTTPS in production, token expiry, secret rotation.
2. Decide: for this lesson, HTTP on localhost is OK; document what must change for production.

**Check:** You can explain why “returning a password in JSON” is wrong.

---

## Phase 1 — Users & password foundations (shared by all mechanisms)

### Step 1.1 — User model
1. Add a `User` persistence model (MySQL table and/or Mongo collection — match Lesson 02).
2. Minimum fields: unique username or email, hashed password, role (e.g. `user` / `admin`), active flag, timestamps.
3. Do **not** store plaintext passwords.

### Step 1.2 — Password hashing
1. Add a password hashing library appropriate for production-style hashing (research current FastAPI tutorial recommendation).
2. Implement `hash_password` and `verify_password` helpers.
3. In notes: *Why bcrypt/argon2 instead of SHA256 alone?*

### Step 1.3 — Auth schemas
1. Create Pydantic models: register, login, public user response (never include password hash).
2. Create a register endpoint (open) and confirm hash is what gets saved.

**Check:** Register a user; DB shows a hash, not the raw password; login verification helper returns True/False correctly in a small test.

### Step 1.4 — Roles for authorization
1. Define at least two roles: `user`, `admin`.
2. Decide rules for Books, for example:
   - any authenticated user: create / read / update own… (or all reads)
   - admin only: delete (or manage any book)
3. Write the rules down — you will enforce them in dependencies later.

---

## Phase 2 — Shared FastAPI security building blocks

### Step 2.1 — `get_current_user` dependency (target design)
1. Plan a dependency that resolves the current user from the active auth mechanism.
2. Plan `require_roles("admin")` (or similar) that raises `403` if the role is insufficient.
3. In notes: *401 vs 403 — when each?*

### Step 2.2 — Protect Books routes gradually
1. Leave `/` health public.
2. Make mutating Books routes authenticated first; then tighten deletes to admin.
3. Keep OpenAPI security schemes updated so `/docs` can authorize (Authorize button).

**Check:** You know which routes will be public vs authenticated vs admin-only.

---

## Part A — Session-based authentication

> Complete Part A before Part B.

---

## Phase 3A — Sessions

### Step 3A.1 — Server-side session store
1. Choose a session backend for learning:
   - signed cookie session middleware (simple), **or**
   - server store (Redis / DB) for “real” sessions
2. Add session secret to `.env` (long random string); load via settings.
3. In notes: *What does signing a cookie protect against? What does it not protect against?*

### Step 3A.2 — Login / logout with sessions
1. `POST /auth/session/login` — verify credentials; on success, store `user_id` (and maybe role) in the session.
2. `POST /auth/session/logout` — clear session.
3. `GET /auth/session/me` — return current user from session; `401` if missing.

**Check:** Login sets a cookie; `/me` works in browser or a client that stores cookies; logout makes `/me` fail.

### Step 3A.3 — Session dependency
1. Implement `get_current_user_from_session`.
2. Apply it to selected Books routes.
3. Confirm unauthenticated requests get `401`.

### Step 3A.4 — CSRF awareness (important)
1. Read briefly about CSRF and cookie-based auth.
2. For this lesson: document the risk; optionally add a simple CSRF mitigation if you use cookie sessions for state-changing requests.
3. In notes: *Why are Bearer tokens in Authorization headers less exposed to classic CSRF?*

**Check:** You can demonstrate one authenticated Books write using session cookies.

---

## Part B — JWT authentication

---

## Phase 3B — JWT access tokens

### Step 3B.1 — Token design
1. Decide claims at minimum: subject (`sub` = user id), expiry (`exp`), maybe `role`.
2. Choose algorithm (e.g. HS256 for learning with a secret; know that RS256 exists for asymmetric keys).
3. Put `JWT_SECRET` / algorithm / expire minutes in settings (not hardcoded).

### Step 3B.2 — Issue tokens
1. `POST /auth/jwt/login` (or OAuth2 password form compatible endpoint for Swagger).
2. On success, return `{ "access_token": "...", "token_type": "bearer" }`.
3. Do not put sensitive data you would regret leaking into the JWT payload (JWTs are signed, not encrypted by default).

**Check:** You can decode the token on jwt.io (dev only) and see `exp` / `sub`; tampering fails verification in your app.

### Step 3B.3 — Protect routes with Bearer JWT
1. Use FastAPI security utilities (`HTTPBearer` or `OAuth2PasswordBearer`).
2. Implement `get_current_user_from_jwt`: extract token → verify → load user → return.
3. Invalid / expired / missing token → `401` with `WWW-Authenticate` where appropriate.

**Check:** `/docs` Authorize with Bearer works; protected Books routes succeed with token and fail without.

### Step 3B.4 — Refresh tokens (optional but recommended)
1. Add a longer-lived refresh token strategy (store hash server-side if you want revocation).
2. `POST /auth/jwt/refresh` issues a new access token.
3. In notes: *Why short-lived access tokens + refresh is common?*

### Step 3B.5 — Revocation & logout reality check
1. Document: pure stateless JWT cannot be truly “logged out” until expiry unless you add a blocklist / version field.
2. Implement one simple approach (blocklist in DB/memory for learning, or token version on user).

---

## Part C — OAuth 2.0 (external login)

---

## Phase 3C — Login with an identity provider

### Step 3C.1 — Pick a provider
1. Choose one: Google, GitHub, or Auth0 / similar — whatever you can create a free OAuth app for.
2. Create OAuth client credentials; put client id/secret and redirect URI in `.env`.
3. Register redirect URL carefully (e.g. `http://127.0.0.1:8000/auth/oauth/callback`).

### Step 3C.2 — Authorization code flow (conceptual steps)
Write the flow in your notes before coding:

1. User hits “Login with Provider”
2. Redirect to provider consent screen
3. Provider redirects back with `code`
4. Your backend exchanges `code` for tokens
5. Your backend fetches profile (email / id)
6. Your backend finds or creates a local `User`
7. Your backend establishes **your** session or issues **your** JWT

### Step 3C.3 — Implement start + callback routes
1. `GET /auth/oauth/login` — redirect to provider.
2. `GET /auth/oauth/callback` — handle `code`, create/link user, then issue session **or** JWT (reuse Part A or B).
3. Handle errors: denied consent, invalid state, token exchange failure.

**Check:** You can log in via provider in a browser and then call a protected Books route.

### Step 3C.4 — State parameter & security
1. Use a `state` value to mitigate CSRF on the OAuth redirect.
2. In notes: *What attack does `state` help prevent?*

### Step 3C.5 — Scopes
1. Request only the scopes you need (e.g. email profile).
2. In notes: *Why is “request all scopes” a bad default?*

---

## Phase 4 — Authorization on Books API

### Step 4.1 — Apply role checks
1. Add dependencies so `DELETE /books/{id}` requires `admin` (or your chosen rule).
2. Authenticated non-admin gets `403`, anonymous gets `401`.

### Step 4.2 — Ownership (optional stretch)
1. Add `owner_id` on Book.
2. Allow update only if `current_user.id == book.owner_id` or user is admin.
3. In notes: *How is ownership different from roles?*

### Step 4.3 — Consistency across auth modes
1. Whether the user arrived via session, JWT, or OAuth, authorization rules for Books should be the same.
2. Prefer one `get_current_user` abstraction that delegates to the active scheme, or separate clearly named dependencies used by routes.

---

## Phase 5 — OpenAPI, testing, and hygiene

### Step 5.1 — Swagger security schemes
1. Configure security so `/docs` supports:
   - Bearer JWT for Part B
   - (Sessions are cookie-based — test with browser or a cookie-aware client)
2. Document how to try each flow.

### Step 5.2 — Manual test matrix
Create a small checklist (PowerShell / curl / httpie) covering:

| Case | Expected |
|------|----------|
| Register + session login + GET /me | 200 |
| JWT login + protected create book | 201 |
| No credentials on protected route | 401 |
| User role on admin delete | 403 |
| Admin delete | 204 |
| OAuth login happy path | lands authenticated |
| Expired / tampered JWT | 401 |

### Step 5.3 — Production checklist (notes only)
Write what you would change before production:

- [ ] HTTPS only
- [ ] Secure / HttpOnly / SameSite cookie flags
- [ ] Strong secrets from a vault / env
- [ ] Token TTL & rotation
- [ ] Rate limit login endpoints
- [ ] Audit lockouts / password reset (future)

---

## Phase 6 — Compare mechanisms (learning outcome)

Complete after implementing all three:

| Question | Your answer |
|----------|-------------|
| Best for first-party browser app on same site? | |
| Best for mobile / SPA calling your API? | |
| Best when you do not want to store passwords? | |
| Easiest to revoke immediately? | |
| Hardest part you hit while implementing? | |

In notes: *Could you combine OAuth login with JWT access for your API? When is that useful?*

---

## Phase 7 — Self-review checklist

Before you call Lesson 03 done, confirm:

- [ ] Users persist with hashed passwords (or passwordless via OAuth-only accounts)
- [ ] Session login / logout / me works with cookies
- [ ] JWT login + Bearer-protected routes work (including via `/docs`)
- [ ] OAuth authorization-code login works with one provider
- [ ] Books routes enforce authn; at least one route enforces authz (role)
- [ ] 401 vs 403 used correctly
- [ ] Secrets only in `.env` / settings; nothing sensitive in git
- [ ] You can explain sessions vs JWT vs OAuth in your own words
- [ ] You documented CSRF, token expiry, and logout/revocation tradeoffs

---

## What to do next (optional future lessons)

- Lesson 04 ideas: refresh-token rotation hardening, API keys, RBAC/ABAC, rate limiting, CORS for SPAs, HTTPS local certs, audit logs.
- Lesson 05 ideas: testing auth with `TestClient`, CI secrets, deployment.

---

## How to use this file

1. Finish Phase 0–2, then **Part A → Part B → Part C** in order.
2. After each part, protect at least one Books endpoint with that mechanism before moving on.
3. If stuck for more than ~20 minutes, re-read the FastAPI Security tutorial section for that mechanism, then ask for a **hint** (not the full solution) for that step only.
