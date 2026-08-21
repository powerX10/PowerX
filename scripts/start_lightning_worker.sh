#!/usr/bin/env bash
set -euo pipefail
: "${POWERX_CACHE_ROOT:=$HOME/.cache/powerx}"
: "${POWERX_MAX_LOADED_MODELS:=1}"
export POWERX_CACHE_ROOT POWERX_MAX_LOADED_MODELS
exec uvicorn apps.lightning_worker.main:app --host 0.0.0.0 --port "${PORT:-8081}"
