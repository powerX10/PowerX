# PowerX Phase 11 Termux Compatibility Fix

This patch fixes the Android/Termux Python 3.14 failure caused by pydantic-core
being compiled from source and killed during the Rust/maturin build.

Changes:
- Replaces the Phase 9 core model DTO dependency on Pydantic with stdlib dataclasses.
- Preserves the `model_validate()` and `model_dump()` API used by Phase 9-11.
- Keeps CMS CPU/GPU/mobile/cloud routing fully dynamic.
- Makes Phase 11 scripts runnable directly without manually setting PYTHONPATH.
- Splits Termux-safe core requirements from optional FastAPI/Pydantic API-host requirements.

The API-host dependency file is `requirements-phase11-api.txt`. Do not install it
on Termux unless the environment has a compatible pydantic-core wheel/build setup.
