#!/data/data/com.termux/files/usr/bin/bash
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
cd "$ROOT"
exec python -m uvicorn apps.powerx_final_api.main:app --host "${POWERX_API_HOST:-0.0.0.0}" --port "${POWERX_API_PORT:-8080}"
