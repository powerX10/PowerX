# PowerX Mobile Runtime — Termux/Android

This runtime uses a real `llama-server` binary on the Android device.

The model stays on the user's phone only when the mobile fallback feature is enabled.
PowerX can call the local server over `127.0.0.1`.

Recommended:
- 1B–4B quantized GGUF model
- 2–3.5GB model file for mainstream 6–12GB RAM phones
- start with `scripts/mobile_detect.py`
- validate model before starting

The runtime never downloads a model automatically. The application can later provide
an explicit model-download/consent flow.
