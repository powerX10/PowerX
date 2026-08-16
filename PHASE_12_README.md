# PowerX Phase 12 — Runtime Fabric Activation

Phase 12 turns the Phase 1–11 code/warehouse into a provider-aware runtime fabric.

## Intended routing

- Normal server workloads: **Modal CPU → Beam CPU fallback**.
- Small eligible user tasks: **mobile edge first**, then CPU fallback.
- Heavy/vision workloads: **GPU16 preferred**.
- Image/video generation: **GPU16 only by default**.
- 24×7 market scanning/backtest/orchestration: **CPU runtime class**.
- Google Drive remains the warehouse/disk; compute happens on runtime nodes.

## No hardcoded endpoints

All endpoint URLs and tokens are read from environment variables referenced by
`config_phase12/runtime_fabric.json`. Provider priority can be changed in config/CMS.

## Important operational distinction

This phase contains deployable provider templates and routing/market code, but a
provider is not live until its credentials are configured and its deployment command
has been run. Colab is treated as an optional GPU worker, not a guaranteed 24×7 server.

## Validation

`python -m unittest discover -s tests_phase12 -v`

`python scripts_phase12/apply_cpu_first_policy.py`

`python scripts_phase12/phase12_readiness.py`
