.PHONY: help env check-env db db-down dev-be dev-fe migrate up down lint test fmt \
	lint-be lint-fe test-be test-fe fmt-be fmt-fe

COMPOSE := docker compose -f infra/docker/compose.local.yaml --project-directory . --env-file .env

# Loads the root .env into the recipe's shell (process env only — the app
# itself never reads .env files). See docs/architecture/env.md.
LOAD_ENV = set -a; . ./.env; set +a;

help:
	@echo "Targets:"
	@echo "  env       - create .env from .env.example if missing (never overwrites)"
	@echo "  db        - start postgres (docker compose up -d --wait postgres)"
	@echo "  db-down   - stop postgres (keeps the volume)"
	@echo "  dev-be    - run the backend locally (uv run python -m app.run)"
	@echo "  dev-fe    - run the frontend locally (pnpm dev)"
	@echo "  migrate   - run backend migrations (alembic upgrade head)"
	@echo "  up        - build and start api+web+postgres (profile app)"
	@echo "  down      - stop api+web only (postgres keeps running)"
	@echo "  lint      - lint be (ruff, ty) and fe (eslint, tsc)"
	@echo "  test      - test be (pytest) and fe (none yet)"
	@echo "  fmt       - format be (ruff format) and fe (prettier)"

env:
	@if [ -f .env ]; then \
		echo ".env already exists, leaving it as is"; \
	else \
		cp .env.example .env; \
		echo "Created .env from .env.example"; \
	fi

check-env:
	@test -f .env || { echo "copy .env.example to .env"; exit 1; }

db: check-env
	$(COMPOSE) up -d --wait postgres

db-down: check-env
	$(COMPOSE) stop postgres

dev-be: check-env
	$(LOAD_ENV) cd be && uv run python -m app.run

dev-fe: check-env
	$(LOAD_ENV) cd fe && pnpm dev

migrate: check-env
	$(LOAD_ENV) cd be && uv run alembic upgrade head

up: check-env
	$(COMPOSE) --profile app up -d --build --wait

down: check-env
	$(COMPOSE) --profile app rm -sf api web

lint: lint-be lint-fe

lint-be:
	cd be && uv run ruff check . && uv run ty check

lint-fe:
	cd fe && pnpm lint && pnpm typecheck

test: test-be test-fe

test-be: check-env
	$(LOAD_ENV) cd be && uv run pytest -q

test-fe: check-env
	@echo "fe: no test suite yet (pnpm typecheck runs under 'make lint')"

fmt: fmt-be fmt-fe

fmt-be:
	cd be && uv run ruff format .

fmt-fe:
	cd fe && pnpm format
