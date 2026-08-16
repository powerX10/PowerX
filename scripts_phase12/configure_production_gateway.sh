#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

CPU_URL="${POWERX_MODAL_CPU_URL:-https://tradewithzara63--powerx-modal-cpu-api.modal.run}"
BROKER_URL="${POWERX_BROKER_URL:-https://tradewithzara63--powerx-runtime-broker-api.modal.run}"
WORKER_TOKEN="$(cat "$HOME/.config/powerx/worker_token")"

KEY_FILE="$HOME/.config/powerx/production_api_key"
mkdir -p "$(dirname "$KEY_FILE")"
if [ ! -s "$KEY_FILE" ]; then
  python - <<'PY' > "$KEY_FILE"
import secrets
print(secrets.token_urlsafe(48))
PY
  chmod 600 "$KEY_FILE"
fi
PROD_KEY="$(cat "$KEY_FILE")"

modal secret create powerx-runtime   POWERX_MODAL_CPU_URL="$CPU_URL"   POWERX_MODAL_CPU_TOKEN="$WORKER_TOKEN"   POWERX_BROKER_URL="$BROKER_URL"   POWERX_WORKER_TOKEN="$WORKER_TOKEN"   POWERX_PRODUCTION_API_KEY="$PROD_KEY"   POWERX_DEFAULT_CHAT_MODEL="qwen25-3b-general"

unset WORKER_TOKEN PROD_KEY

echo "powerx-runtime secret configured."
