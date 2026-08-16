# PowerX Phase 11 — Final Integration Layer

Phase 11 is additive: it does not overwrite Phase 1–10 paths. It joins the Drive warehouse, Phase 9 CMS, Phase 10 trading swarm, runtime endpoints and the unified PowerX API.

## What it finishes in code

- Registers the exact 01–20 warehouse roster in the CMS.
- Preserves owner-edited CMS runtime bindings instead of hardcoding CPU/GPU/mobile/cloud.
- Maps all 20 models to capabilities needed by chat, coding, trading, chart vision, finance sentiment, forecasting, retrieval, STT, TTS, image and video.
- Provides Drive-on-demand staging via the already configured `PowerXWarehouse` rclone remote.
- Adds a runtime supervisor whose adapter launch command can be controlled in CMS binding metadata.
- Adds a single unified API (`:8500`) for chat, media, speech and trading analysis.
- Adds runtime health/failover and a final readiness audit.
- Uses built-in `unittest`; pytest is not required for Phase 11 validation.

## Important boundary

The software integration can be final, but infrastructure cannot be embedded into a ZIP: a GPU/CPU/mobile runtime must actually be online, its endpoint must be configured in the CMS, and required secrets/tokens must exist. Colab is session-based rather than an always-on production GPU. `gpt-oss-120b` is not part of this 01–20 roster and can be added later through the CMS without changing this architecture.

## Merge

```bash
cd ~/PowerX
unzip -o '/storage/emulated/0/Download/PowerX_Phase_11_FINAL.zip'
python -m compileall -q powerx/final_runtime apps/powerx_final_api scripts_final
python -m unittest discover -s tests_phase11 -v
python scripts_final/sync_final_registry.py
python scripts_final/final_readiness.py
```

Then validate the existing Next.js app:

```bash
cd ~/PowerX/apps/control_center
npm run typecheck
npm run build
```

## Runtime activation

Set runtime endpoints/bindings in the Phase 9 CMS. Endpoints are deliberately not hardcoded. To start the final unified API:

```bash
export POWERX_CONTROL_TOKEN='your-existing-control-token'
bash ~/PowerX/scripts_final/start_final_api.sh
```

Final API base: `http://<host>:8500`.
