#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$HOME/PowerX";mkdir -p "$HOME/.config/powerx"
if [ ! -s "$HOME/.config/powerx/node_token" ]; then python - <<'PY'
import secrets,pathlib
p=pathlib.Path.home()/".config/powerx/node_token";p.write_text(secrets.token_urlsafe(48));p.chmod(0o600)
PY
fi
T="$(cat "$HOME/.config/powerx/node_token")";cd apps/control_center
npx vercel@latest env rm POWERX_NODE_TOKEN production -y 2>/dev/null || true
printf '%s' "$T" | npx vercel@latest env add POWERX_NODE_TOKEN production
echo "Runtime broker token configured."
