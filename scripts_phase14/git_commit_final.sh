#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$HOME/PowerX"
git add powerx/ma powerx/final_product apps/ma_api apps/powerx_production_api  apps/control_center/lib/powerx.ts apps/control_center/app/api/powerx/chat/route.ts  deploy_phase13 integrations/powerx_unified scripts_phase13 scripts_phase14 tests_phase13 tests_phase14  PHASE_13_MANIFEST.json PHASE_13_README.md PHASE_14_MANIFEST.json PHASE_14_README.md
git commit -m "Complete PowerX MA 20-model orchestration and final product runtime"
git push origin main
git status
