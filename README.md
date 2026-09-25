# saju

FastAPI backend (`be/`) + Next.js frontend (`fe/`) + PostgreSQL, orchestrated
with Docker Compose. See `AGENTS.md` for project conventions and routing.

## Quick start

```sh
cp .env.example .env
cp be/.env.example be/.env
cp fe/.env.example fe/.env

make db          # start postgres only (127.0.0.1:5433)
make migrate     # apply backend migrations
make dev-be      # run the backend locally (127.0.0.1:8000)
make dev-fe      # run the frontend locally (127.0.0.1:3000), in another shell
```

Or run everything in containers:

```sh
make up          # build + start api, web, postgres
make down        # stop api+web (postgres keeps running)
```

## Checks

```sh
make lint
make test
make fmt
```

See `be/README.md` and `fe/README.md` for per-app details.
