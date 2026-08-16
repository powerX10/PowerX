# Phase 12 Modal CPU build fix

Installs CPU-only PyTorch 2.9.1 from the official PyTorch CPU wheel index, adds pip resume retries/timeouts, and avoids FastAPI's unnecessary `standard` extras.
