# PowerX Phase 12 Modal Real Inference Patch

Replaces the Phase 12 Modal CPU stub with a real CPU inference worker.

Supported adapters:
- llamacpp (GGUF text/chat)
- transformers_text_classification
- transformers_text_generation
- sentence_transformers
- transformers_reranker
- chronos
- whisper / transformers_asr

The worker stages models on demand from the configured PowerX rclone warehouse
into the persistent Modal Volume `/cache`.

Specialized adapters not implemented here intentionally return HTTP 422 so the
runtime fabric can fail over instead of pretending inference succeeded.
