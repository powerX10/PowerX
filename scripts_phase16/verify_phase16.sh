#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$HOME/PowerX";export PYTHONPATH="$HOME/PowerX"
python scripts_phase16/ensure_firebase_admin_export.py
python -m unittest discover -s tests_phase16 -v
python -m compileall -q powerx deploy_phase16
cd apps/control_center;npm run typecheck;npm run build
