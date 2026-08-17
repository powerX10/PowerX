#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$HOME/PowerX";export PYTHONPATH="$HOME/PowerX"
python -m py_compile deploy_phase12/mobile_edge/worker.py deploy_phase12/mobile_edge/local_inference.py deploy_final_fix/server_cpu_node/worker.py
bash scripts_final_fix/configure_runtime.sh
cd apps/control_center;npm run typecheck;npm run build
cd "$HOME/PowerX";npx vercel@latest deploy --prod
bash scripts_final_fix/start_mobile.sh
git add POWERX_FINAL_FIX_README.md FINAL_FIX_MANIFEST.json apps/control_center deploy_phase12/mobile_edge/worker.py deploy_phase12/mobile_edge/local_inference.py deploy_final_fix scripts_final_fix
git commit -m "Final PowerX phone-first runtime broker, CPU fallback and connected UI" || true
git push origin main
git status
echo "=== MOBILE HEALTH ===";curl -sS --max-time 15 http://127.0.0.1:8080/health||true
