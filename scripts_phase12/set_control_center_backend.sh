#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 https://...modal.run"
  exit 2
fi

URL="${1%/}"
ENV_FILE="$HOME/PowerX/apps/control_center/.env.local"
KEY_FILE="$HOME/.config/powerx/production_api_key"

if [ ! -s "$KEY_FILE" ]; then
  echo "Missing $KEY_FILE. Run configure_production_gateway.sh first."
  exit 1
fi

python - "$ENV_FILE" "$URL" "$KEY_FILE" <<'PY'
from pathlib import Path
import sys

env_path = Path(sys.argv[1])
url = sys.argv[2]
key = Path(sys.argv[3]).read_text().strip()

lines = env_path.read_text().splitlines() if env_path.exists() else []
values = {
    "POWERX_PRODUCTION_API_URL": url,
    "POWERX_PRODUCTION_API_KEY": key,
}
out = []
seen = set()
for line in lines:
    if "=" in line and not line.lstrip().startswith("#"):
        k = line.split("=", 1)[0].strip()
        if k in values:
            out.append(f"{k}={values[k]}")
            seen.add(k)
            continue
    out.append(line)
for k, v in values.items():
    if k not in seen:
        out.append(f"{k}={v}")
env_path.write_text("\n".join(out).rstrip() + "\n")
print(f"Updated {env_path}")
PY
