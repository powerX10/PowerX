#!/usr/bin/env bash
set -euo pipefail

mkdir -p logs data

if [ -z "${POWERX_API_KEY:-}" ]; then
  echo "POWERX_API_KEY missing"; exit 1
fi

echo "Starting PowerX Final API..."
exec uvicorn apps.final_api.main:app --host "${POWERX_HOST:-0.0.0.0}" --port "${POWERX_PORT:-8000}"
