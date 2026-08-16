#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$HOME/PowerX"
python -m compileall -q powerx/ma powerx/final_product apps/ma_api apps/powerx_production_api deploy_phase13
python -m unittest discover -s tests_phase13 -v
python -m unittest discover -s tests_phase14 -v
cd apps/control_center
npm run typecheck
npm run build
cd "$HOME/PowerX"
python scripts_phase14/final_acceptance.py
