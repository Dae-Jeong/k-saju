#!/usr/bin/env bash
# 서버 cron 에서 매일 실행: DB 를 덤프해 ~/backups 에 14일 보관한다.
set -euo pipefail
cd "$(dirname "$0")/../.."
set -a; . infra/docker/.env.prod; set +a
DIR="$HOME/backups/saju"; mkdir -p "$DIR"
docker exec saju-postgres pg_dump -U "$DB_USERNAME" -d "$DB_NAME" -Fc > "$DIR/saju-$(date +%F).dump"
find "$DIR" -name 'saju-*.dump' -mtime +14 -delete
