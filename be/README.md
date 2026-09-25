# API

FastAPI + uv + PostgreSQL backend skeleton. Python version is pinned in
`.python-version`; dependencies are managed in `pyproject.toml` and `uv.lock`.
`src/app/` is the application's import package (distribution name is `api`).

## Setup

```sh
uv sync
cp .env.example .env
uv run alembic upgrade head
uv run python -m app.run
```

Defaults to `127.0.0.1:8000`. Change `SERVER_PORT` in `.env` for an isolated
run (see the machine's local dev conventions for reserved ports).

- `GET /`: `{"data":{"message":"Hello, API!"}}`
- `GET /health/live`: liveness, always 200
- `GET /health/ready`: readiness; pings the DB per request, 200 when reachable
  and a `application/problem+json` 503 (`DATABASE_UNAVAILABLE`) when not
- `/docs`: Swagger UI, `/openapi.json`: OpenAPI spec

## Environment

`.env.example` is the shared template; `.env` is local-only and untracked.
Process env vars > `.env` > code defaults, in that priority.

| Setting | Role |
| --- | --- |
| `APP_NAME` | OpenAPI title / logs |
| `SERVICE_VERSION` | OpenAPI version / logs |
| `APP_ENVIRONMENT` | Logged environment name; default `local` |
| `SERVER_HOST` / `SERVER_PORT` | Bind address |
| `SHUTDOWN_TIMEOUT_SECONDS` | Graceful shutdown request drain budget |
| `LOG_LEVEL` | App + Uvicorn log level (lowercase) |
| `DB_HOST` / `DB_PORT` / `DB_NAME` / `DB_USERNAME` / `DB_PASSWORD` | PostgreSQL connection; combined into an async `postgresql+asyncpg://` URL |
| `DB_POOL_SIZE` / `DB_POOL_MAX_OVERFLOW` / `DB_POOL_TIMEOUT_SECONDS` | SQLAlchemy async engine pool |

Settings are validated once at startup (`app/core/settings.py`) and passed
explicitly; invalid config exits without echoing raw input.

## Structure

Role folders, one file per feature inside each:

| Path | Role |
| --- | --- |
| `run.py` | Process entrypoint: settings, logging, Uvicorn |
| `bootstrap/` | `app.py` assembles the app (routers, error handlers); `lifespan.py` + `contracts.py` own startup/shutdown resource lifetime |
| `routers/` | HTTP input/output; `index.py`, `health.py` |
| `schemas/` | `responses.py` — success envelope, Problem Details, error codes |
| `exceptions/` | `application.py` — `ApplicationError`, the common expected-failure base |
| `http/` | `errors.py` — exception → Problem Details HTTP mapping, OpenAPI response docs |
| `dependencies/` | `database.py` — request-scoped `AsyncSession`; `clock.py` — `Clock` provider |
| `core/` | `settings.py`, `database.py` (engine/session factory), `logging.py` (structured JSON logs), `clock.py`, `contracts.py` |
| `services/`, `contracts/`, `repositories/`, `models/`, `validation/` | Empty role packages, ready for the first feature |
| `domain/saju/` | Placeholder for pure saju calculation logic — no HTTP/DB/framework imports |
| `migrations/`, `alembic.ini` | Async Alembic scaffold; targets `app.models.metadata` |

Import direction: `routers` → `services` → `repositories`/`models`; `core`
never imports from higher layers; `bootstrap` wires concrete implementations
but owns no business logic.

## Build and verification

```sh
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest -q
```

`tests/conftest.py` isolates each test's working directory and strips
`Settings`-related env vars so personal `.env` files never leak in. DB-backed
tests (see `tests/routers/test_health.py`) check connectivity first via the
`db_available` fixture and skip cleanly when no local Postgres is reachable,
instead of failing.

## Container

```sh
docker build -t api .
docker run --rm -p 8000:8000 --env-file .env api
```

`scripts/start.sh` runs `alembic upgrade head` then starts the app; the
container's `HEALTHCHECK` polls `/health/ready`.
