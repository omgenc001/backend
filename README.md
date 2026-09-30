<div align="center">

# ⚡ FastAPI Auth Backend

**A production-shaped authentication API built with FastAPI, SQLAlchemy and PostgreSQL.**

Email/password signup, login and JWT-protected routes — laid out in clean, layered modules.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.142.1-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.1.1-D71F00)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18%2B-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT%20HS256-000000?logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![License](https://img.shields.io/badge/License-Not%20specified-lightgrey)](#-license)

</div>

---

## 📖 Overview

This is the **backend service** for a game/web application's user accounts. It exposes a small, focused
REST surface that handles the full credential lifecycle:

- Create an account with a unique email
- Hash the password with **bcrypt** before it ever touches the database
- Exchange credentials for a signed **JWT access token**
- Validate that token on protected endpoints and resolve it back to a database user

Everything is written as plain synchronous FastAPI + SQLAlchemy, so it stays easy to read, easy to
debug, and fast to boot — no async plumbing required to get started.

## ✨ Features

| | Feature |
|---|---|
| 🔐 | **Signup** with duplicate-email protection (unique index + `409 Conflict`) |
| 🧂 | **bcrypt** password hashing with per-password salt (`gensalt()`), never stored in plaintext |
| 🎫 | **JWT access tokens** (`HS256`) carrying an expiry claim |
| 🛡️ | **Reusable route dependency** (`restrict_route`) that authenticates `Authorization: Bearer <token>` |
| 🧱 | **Layered architecture** — routes / schemas / models / security kept in separate modules |
| ✅ | **Pydantic v2 validation** with `EmailStr` email verification on every payload |
| 🗄️ | **PostgreSQL** via SQLAlchemy with UUID primary keys |
| 📚 | **Auto-generated OpenAPI docs** at `/docs` (Swagger UI) and `/redoc` (ReDoc) |
| ⚙️ | **12-factor config** — all secrets and connection strings loaded from `.env` |

## 🧰 Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.10+ (developed on 3.14.6) |
| Web framework | FastAPI | 0.142.1 |
| ASGI server | Uvicorn | 0.54.0 |
| ORM | SQLAlchemy | 2.1.1 |
| Database | PostgreSQL | 18+ (verified on 18.6) |
| DB driver | psycopg2-binary | 2.9.13 |
| Validation | Pydantic / pydantic-core | 2.13.5 / 2.46.5 |
| Email validation | email-validator | 2.3.0 |
| Hashing | bcrypt | 5.0.0 |
| Tokens | python-jose | 3.5.0 |
| Config | python-dotenv | 1.2.3 |

## 📂 Project Structure

```text
backend/
├── app/
│   ├── db/
│   │   ├── db_connections.py    # engine, SessionLocal, Base, get_db() dependency
│   │   └── tables.py            # SQLAlchemy models (User)
│   ├── encrption/               # security helpers
│   │   ├── encrption.py         # hash_password() / verify_password()  (bcrypt)
│   │   └── jwt.py               # create_access_token() / verify_token() / restrict_route()
│   ├── routes/
│   │   └── auth.py              # /signup, /login, /check_login endpoints
│   ├── schemas/
│   │   └── users.py             # Pydantic request/response models
│   └── main.py                  # FastAPI app instance, router registration, table creation
├── settings/
│   └── load_env.py              # loads .env and exports typed config constants
├── .env                         # local secrets — NOT committed (see .env.example)
├── .env.example                 # template for the required environment variables
├── .gitignore
├── requirement.txt              # pinned dependency list
└── README.md
```

> **Request lifecycle:**
> `HTTP request` → `route handler` → `get_db()` session → `table model (SQLAlchemy)` →
> `Pydantic response model` → `JSON response`.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** — verify with `python --version`
- **PostgreSQL 18+** running locally (or any reachable PostgreSQL instance) — verified on 18.6
- **pip** and **git**

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create and activate a virtual environment

```bash
# Windows (PowerShell)
python -m venv dev_mode
.\dev_mode\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv dev_mode
source dev_mode/bin/activate
```

> The virtual environment is named `dev_mode` in this project. If PowerShell blocks the activation
> script, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.

### 3. Install dependencies

```bash
pip install -r requirement.txt
```

⚠️ **`requirement.txt` is currently incomplete.** The application imports `bcrypt`, `SQLAlchemy`,
`psycopg2` and `python-jose`, but those four are not listed in the file yet, so a fresh install will
fail on import. Install them alongside the pinned list until the file is regenerated:

```bash
pip install bcrypt==5.0.0 SQLAlchemy==2.1.1 psycopg2-binary==2.9.13 python-jose==3.5.0
```

### 4. Create the database

```bash
# psql shell
psql -U postgres -c "CREATE DATABASE auth;"
```

Or create a database named `auth` with any GUI client (pgAdmin, DBeaver, TablePlus…). The `users`
table is created automatically at application startup by `Base.metadata.create_all(bind=engine)`
from `app/main.py` — **no manual schema or migration step is needed.**

### 5. Configure environment variables

Copy the template and fill in your own values:

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

| Variable | Required | Example | Description |
|---|---|---|---|
| `SQLALCHEMY_URL` | ✅ | `postgresql://postgres:123456@localhost:5432/auth` | Full SQLAlchemy database URL |
| `SECRET_KEY` | ✅ | *(long random string)* | HMAC secret used to sign/verify JWTs |
| `ALGORITHM` | ✅ | `HS256` | JWT signing algorithm |
| `ACCESS_TIME` | ✅ | `30` | Token lifetime **in days** |

Generate a strong secret key with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

> `.env` is listed in `.gitignore` — never commit real credentials. The values used in this README
> are local development placeholders only.

### 6. Run the development server

```bash
uvicorn app.main:dev_mode --reload
```

| Service | URL |
|---|---|
| API base | http://127.0.0.1:8000 |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI schema | http://127.0.0.1:8000/openapi.json |

A quick sanity check:

```bash
curl http://127.0.0.1:8000/
# {"message":"Hello World"}
```

---

## 📡 API Reference

Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Auth | Success | Error responses |
|---|---|---|---|---|
| `GET` | `/` | — | `200` `{"message": "Hello World"}` | — |
| `POST` | `/signup` | — | `201` created user | `409` email already registered · `422` invalid payload |
| `POST` | `/login` | — | `200` user + access token | `401` bad credentials · `422` invalid payload |
| `POST` | `/check_login` | `Bearer` | `200` current user | `401` missing/invalid/expired token |

### `POST /signup`

Creates a new account. The password is bcrypt-hashed before insertion; the stored hash is never
returned to the client.

**Request body**

```json
{
  "email": "player@example.com",
  "player_name": "night_raider",
  "password": "SuperSecret123"
}
```

**Response `201 Created`**

```json
{
  "email": "player@example.com",
  "player_name": "night_raider"
}
```

**Duplicate email → `409 Conflict`**

```json
{ "detail": "User already exists" }
```

### `POST /login`

Verifies the password against the stored bcrypt hash and issues a signed JWT.

**Request body**

```json
{
  "email": "player@example.com",
  "password": "SuperSecret123"
}
```

**Response `200 OK`**

```json
{
  "email": "player@example.com",
  "player_name": "night_raider",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOGQ0NmNhYS05OGUzLTRiYzUtYjFkYi1lMTMyMjI1Yzc3YmIiLCJleHAiOjE3OTMzNzExMTB9.fCNzb_8Jfh60u30hhKqL9II3Yg1cK_lX6Dt7eK9Q3Bw",
  "token_type": "bearer"
}
```

A wrong password or an unknown email both return an identical body, so the API never leaks whether an
account exists:

```json
{ "detail": "Unauthorized" }
```

### `POST /check_login`

Validates the bearer token and returns the authenticated user record.

**Headers**

```http
Authorization: Bearer <access_token>
```

> ⚠️ This endpoint currently returns `401 Unauthorized` even for a freshly issued, valid token —
> see [Known Issues](#-known-issues--roadmap) for the one-line cause.

---

## 🧪 Usage Examples

### End-to-end flow (bash / curl)

```bash
BASE=http://127.0.0.1:8000

# 1) Create an account
curl -X POST "$BASE/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"player@example.com","player_name":"night_raider","password":"SuperSecret123"}'
# => 201 {"email":"player@example.com","player_name":"night_raider"}

# 2) Log in and capture the token
TOKEN=$(curl -s -X POST "$BASE/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"player@example.com","password":"SuperSecret123"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 3) Call a protected route
curl -X POST "$BASE/check_login" -H "Authorization: Bearer $TOKEN"
```

### End-to-end flow (PowerShell)

```powershell
$BASE = "http://127.0.0.1:8000"

Invoke-RestMethod -Method Post -Uri "$BASE/signup" `
  -ContentType "application/json" `
  -Body '{"email":"player@example.com","player_name":"night_raider","password":"SuperSecret123"}'

$login = Invoke-RestMethod -Method Post -Uri "$BASE/login" `
  -ContentType "application/json" `
  -Body '{"email":"player@example.com","password":"SuperSecret123"}'

$token = $login.access_token

Invoke-RestMethod -Method Post -Uri "$BASE/check_login" `
  -Headers @{ Authorization = "Bearer $token" }
```

### Interactive docs

Open **http://127.0.0.1:8000/docs** and use *Authorize* → *bearerAuth* to paste a token, then execute
any protected endpoint straight from the browser.

## 🔑 Authentication Flow

```text
 ┌──────────┐   POST /signup        ┌──────────────────────────────────────┐
 │  Client  │──────────────────────▶│ bcrypt.hashpw(password) → users row  │
 └──────────┘   ◀── 201 ────────────└──────────────────────────────────────┘
       │
       │        POST /login         ┌──────────────────────────────────────┐
       │───────────────────────────▶│ verify hash ▶ sign JWT {sub, exp}    │
       │   ◀── 200 + access_token ──└──────────────────────────────────────┘
       │
       │  POST /check_login         ┌──────────────────────────────────────┐
       └──── Authorization: Bearer ─▶│ decode JWT ▶ load user from DB      │
                                     └──────────────────────────────────────┘
```

1. **Signup** — the email is checked for uniqueness, the password is salted and hashed with bcrypt,
   then the row is inserted.
2. **Login** — the submitted password is compared with the stored hash via `bcrypt.checkpw`. On
   success a token is created with `create_access_token()`: the payload contains the user id and an
   `exp` claim set to *now + `ACCESS_TIME` days*, signed with `SECRET_KEY`/`ALGORITHM`.
3. **Protected routes** — depend on `restrict_route`. It parses the `Authorization` header, requires
   the `Bearer` scheme, decodes the token, loads the matching `User` from the database, and injects
   that user into the endpoint. Any failure returns `401 Unauthorized`.

To protect a new endpoint, simply add the dependency:

```python
from fastapi import Depends
from app.encrption.jwt import restrict_route

@my_router.get("/me")
def me(current_user = Depends(restrict_route)):
    return {"player_name": current_user.player_name}
```

---

## 🗃️ Data Model

**Table `users`** — defined in `app/db/tables.py`

| Column | Type | Constraints |
|---|---|---|
| `id` | `UUID` | primary key, indexed, auto-generated (`uuid4`) |
| `player_name` | `VARCHAR(25)` | not null |
| `email` | `VARCHAR(255)` | not null, unique, indexed — used as the login identifier |
| `password` | `VARCHAR(255)` | not null — stores the **bcrypt hash**, never the raw password |

## 🛡️ Security Notes

- Passwords are hashed with **bcrypt** using a unique salt per user; `verify_password()` compares the
  submitted password against the stored hash.
- JWT payloads carry only the user id and expiry — no passwords or personal data.
- Login failures return a generic `"Unauthorized"` for both unknown emails and wrong passwords.
- `SECRET_KEY`, database credentials and token lifetime live in `.env`, which is excluded from git.
- Emails are validated by Pydantic's `EmailStr` (backed by `email-validator`) before reaching the DB.

**Not yet implemented — consider adding before production:** HTTPS termination, CORS allow-list, rate
limiting / brute-force protection on `/login`, refresh tokens, email verification, a password
strength policy, token revocation, and JWT `SECRET_KEY` rotation.

---

## 🐞 Known Issues & Roadmap

| Status | Item | Details |
|---|---|---|
| 🐛 | **Protected routes always return `401`** | `create_access_token()` is called with the claim key `sub` (in `app/routes/auth.py`), but `verify_token()` reads `payload.get("id")` (in `app/encrption/jwt.py`) → `None` → `401`. Use the same claim name in both places — `sub` is the JWT standard. |
| 📦 | `requirement.txt` omits runtime dependencies | `bcrypt`, `SQLAlchemy`, `psycopg2` and `python-jose` are imported but not listed. Regenerate with `pip freeze > requirement.txt`. |
| 🙈 | `.gitignore` only ignores `.env` | The `dev_mode/` virtual environment and `__pycache__/` folders are not ignored yet. Add `dev_mode/`, `venv/`, `__pycache__/`, `*.pyc`. |
| ✏️ | Typos in module names | The security package is `app/encrption/` (missing the `y` in *encryption*) and package markers are named `_init_.py` instead of `__init__.py` (imports still resolve through implicit namespace packages). |
| 🧹 | Unused import | `from ast import Pass` in `app/routes/auth.py`. |
| 📝 | `check_login` has no response model | It returns the raw SQLAlchemy `User` object, so the response shape is not documented in OpenAPI. Return a Pydantic model instead. |
| 🔌 | No CORS configuration | A browser frontend on another origin cannot call the API yet — add `CORSMiddleware` in `app/main.py`. |
| 🔁 | No schema migrations | Tables are created with `Base.metadata.create_all()` at import time; introduce **Alembic** once the schema starts evolving. |
| 🔍 | No test suite / CI | Add `pytest` + `httpx` integration tests and a GitHub Actions workflow. |
| 🐳 | No containerization | Add a `Dockerfile` and `docker-compose.yml` (API + PostgreSQL) for one-command startup. |
| 📄 | No license | Choose a license (MIT is a common default) and add a `LICENSE` file so others know how they may use the code. |

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository and create a feature branch: `git checkout -b feature/my-feature`
2. Follow the existing structure — new Pydantic models in `app/schemas/`, new endpoints in
   `app/routes/`, new tables in `app/db/tables.py`.
3. Keep dependencies in sync with `requirement.txt`.
4. Commit with clear messages, e.g. `git commit -m "feat: add password reset endpoint"`
5. Push the branch and open a Pull Request describing the change and how you tested it.

Please never commit real credentials, tokens or `.env` files.

## 📄 License

No license file is currently included in this repository. Until one is added, all rights are reserved
by the author and the code is **not** licensed for reuse or redistribution. To open the project up,
add a `LICENSE` file (the MIT template is a common choice) and update the badge at the top of this
README.

---

<div align="center">

Built with ❤️ using [FastAPI](https://fastapi.tiangolo.com/) and [SQLAlchemy](https://www.sqlalchemy.org/)

⭐ If this project helped you, consider giving it a star!

</div>

