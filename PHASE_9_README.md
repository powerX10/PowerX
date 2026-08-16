# PowerX Phase 9 — Dynamic Model CMS + Runtime Control Plane

This phase removes model/runtime decisions from hardcoded Python profile tables for all new model integrations.

## What it adds
- Persistent model registry (`POWERX_MODEL_CMS_DB`)
- CPU/GPU/mobile/cloud bindings editable at runtime
- Enable/disable models without code changes
- Per-model runtime priority, concurrency, RAM/VRAM limits and launch config
- REST resolver for other PowerX services
- Lightweight owner CMS at `/cms`

Start:
`uvicorn apps.model_cms_api.main:app --host 0.0.0.0 --port 8400`

The existing Phase 1–8 files are not duplicated or overwritten. This is an additive phase.
