.PHONY: help db db-down dev-be dev-fe migrate up down lint test fmt \
	lint-be lint-fe test-be test-fe fmt-be fmt-fe

COMPOSE := docker compose -f infra/docker/compose.local.yaml --project-directory .

help:
	@echo "Targets:"
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

db:
	$(COMPOSE) up -d --wait postgres

db-down:
	$(COMPOSE) stop postgres

dev-be:
	cd be && uv run python -m app.run

dev-fe:
	cd fe && pnpm dev

migrate:
	cd be && uv run alembic upgrade head

up:
	$(COMPOSE) --profile app up -d --build --wait

down:
	$(COMPOSE) --profile app rm -sf api web

lint: lint-be lint-fe

lint-be:
	cd be && uv run ruff check . && uv run ty check

lint-fe:
	cd fe && pnpm lint && pnpm typecheck

test: test-be test-fe

test-be:
	cd be && uv run pytest -q

test-fe:
	@echo "fe: no test suite yet (pnpm typecheck runs under 'make lint')"

fmt: fmt-be fmt-fe

fmt-be:
	cd be && uv run ruff format .

fmt-fe:
	cd fe && pnpm format
