# PowerX Phase 2 — 16GB GPU Runtime

This ZIP is additive. Extract it into the same PowerX root after Phase 1.

It adds a production-oriented local/server GPU runtime for 16GB-class GPUs.

Included:
- GPU capability detection
- managed vLLM process lifecycle
- model runtime profiles
- start/stop/status
- health wait/retry logic
- gpt-oss-20b profile
- Qwen 8B profile
- 4B vision profile

Not included:
- trading logic
- Zerion market logic
- mobile runtime (Phase 3)
- H100/120B runtime (future)
