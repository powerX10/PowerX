# PowerX V2 Zip 2 — 20 completed scope points

1. Remote-worker correction: PowerX API no longer sends an API-host-local model path to Lightning.
2. Lightning worker API with `/health`, `/v1/run`, and `/v1/unload`.
3. Google Drive/rclone warehouse client.
4. Local mounted warehouse fallback.
5. On-demand Drive -> Lightning local model cache.
6. Per-model cache locking to prevent duplicate concurrent downloads.
7. Cache-ready marker so partial copies are not treated as usable models.
8. Optional LRU cache eviction through `POWERX_MAX_CACHE_GB`.
9. CPU/RAM/disk/GPU/VRAM runtime probe.
10. Model manager with lazy loading.
11. Loaded-model LRU eviction and GPU memory cleanup.
12. GGUF text adapter via llama.cpp Python bindings.
13. Transformers causal text-generation adapter.
14. Transformers text-classification adapter for FinBERT-class models.
15. Whisper speech-to-text adapter.
16. Kokoro text-to-speech adapter returning WAV as base64.
17. Worker bearer-token protection.
18. Worker health-check script.
19. Local 20-model inventory verification script.
20. Logic tests for warehouse copy, runtime probe, and adapter registration.

Not claimed in Zip 2: image/video generation, timeseries specialist adapters, autonomous GitHub coding tools, long-form video composer, Zerion execution engine. Those are intentionally later milestones so Zip 2 remains testable instead of pretending unsupported models are working.
