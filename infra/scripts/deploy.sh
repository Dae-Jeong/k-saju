#!/usr/bin/env bash
# 서버에서 실행: 최신 main 을 받아 be 를 빌드·교체한다. 마이그레이션은 컨테이너 시작 시 실행된다.
# 사용 (로컬): make deploy-be
set -euo pipefail
cd "$(dirname "$0")/../.."

git pull --quiet --ff-only origin main
export GIT_SHA=$(git rev-parse --short HEAD)

ENV_FILE=infra/docker/.env.prod
if [ ! -f "$ENV_FILE" ]; then
  sed "s/^DB_PASSWORD=.*/DB_PASSWORD=$(openssl rand -hex 24)/" infra/docker/.env.prod.example > "$ENV_FILE"
  chmod 600 "$ENV_FILE"
  echo "created $ENV_FILE with a random DB password"
fi

docker compose --env-file "$ENV_FILE" -f infra/docker/compose.prod.yaml up -d --build --wait
docker image prune -f >/dev/null

# 매일 03:30 DB 백업 (없을 때만 등록)
LINE="30 3 * * * $PWD/infra/scripts/backup.sh >> $HOME/backups/backup.log 2>&1"
if ! { crontab -l 2>/dev/null || true; } | grep -qF "infra/scripts/backup.sh"; then
  mkdir -p "$HOME/backups"
  { crontab -l 2>/dev/null || true; echo "$LINE"; } | crontab -
fi
docker compose --env-file "$ENV_FILE" -f infra/docker/compose.prod.yaml ps --format "{{.Name}} {{.Status}}"
echo "deployed $GIT_SHA"
