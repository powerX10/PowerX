#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$HOME/PowerX";export PYTHONPATH="$HOME/PowerX"
python scripts_phase15/apply_orchestrator_router_patch.py
python -m compileall -q powerx/ma
cd apps/control_center;npm run typecheck;npm run build
