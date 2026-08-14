# PowerX — Phase 1: Core Orchestration Layer

PowerX is the central AI-model orchestration service.

Phase 1 contains only the core responsibilities:
- model catalog
- runtime capability registry
- automatic task routing
- provider abstraction
- OpenAI-compatible remote inference client
- FastAPI gateway
- health/config endpoints
- strict separation from Zerion X1 trading logic

No trading indicators, strategies, backtesting, broker logic, market feeds,
image generation, or video generation are included in this phase.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn apps.api.main:app --host 0.0.0.0 --port 8000
```

## Test

```bash
python -m unittest discover -s tests -v
```
