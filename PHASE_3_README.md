# PowerX Phase 3 — CPU + Mobile Runtime

Extract this ZIP into the same project root after Phase 1 and Phase 2.

This phase adds only new files. It does not duplicate earlier phase files.

## What it adds

- Real llama.cpp server process management for CPU inference
- Termux/Android on-device llama.cpp runtime
- GGUF model slots for small/medium models
- Local model-file validation
- Device/RAM/storage capability detection
- OpenAI-compatible localhost inference on mobile
- CPU forecasting adapter interface
- embedding/reranking/guard service slots
- runtime discovery so PowerX can choose GPU / CPU / mobile

## Important

No trading logic is in PowerX. Zerion X1 sends tasks/context to PowerX;
PowerX selects a model/runtime and returns model output.

Actual local inference requires:
1. a compatible `llama-server` binary, and
2. a compatible GGUF model file.

The runtime code is real; it never returns fake model output.
