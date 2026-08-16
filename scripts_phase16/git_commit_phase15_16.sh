#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$HOME/PowerX"
git add PHASE_15_MANIFEST.json PHASE_15_README.md PHASE_16_MANIFEST.json PHASE_16_README.md apps/control_center powerx/ma/router.py powerx/mobile_profiles.py deploy_phase16 scripts_phase15 scripts_phase16 tests_phase16
git commit -m "Finish PowerX premium MA workspace, CMS, API platform and mobile profiles"
git push origin main
git status
