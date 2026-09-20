#!/usr/bin/env bash
# TEST-020 — smoke E2E mínimo (TASK-020)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/docker"

echo "== compose ps =="
docker compose ps

echo "== ES =="
curl -fsS "http://localhost:9200" | head -c 200
echo

echo "== ES count =="
curl -fsS "http://localhost:9200/desinfo_events/_count" || echo "(índice ainda não criado — rode seed)"

echo "== Kibana =="
curl -fsS "http://localhost:5601/api/status" | head -c 200
echo

echo "== WordPress =="
curl -fsS -o /dev/null -w "%{http_code}\n" "http://localhost:8080"

echo "== Shiny =="
curl -fsS -o /dev/null -w "%{http_code}\n" "http://localhost:3838/dsn/" || true

echo "Smoke OK (parcial se seed/plugin ainda não ativos)"
