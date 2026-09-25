#!/bin/sh
set -eu

# Docker WORKDIR is /app; Compose supplies the application's environment.
python -m alembic -c /app/alembic.ini upgrade head

exec python -m app.run
