import os, time, secrets
from fastapi import FastAPI, Header, HTTPException
import httpx

from powerx.ma.model_catalog import MODEL_IDS, MODEL_ADAPTERS, CAPABILITY_MODELS

TOKEN = os.getenv("POWERX_CONTROL_TOKEN", "")
CPU_URL = os.getenv("POWERX_MODAL_CPU_URL", "").rstrip("/")
BROKER_URL = os.getenv("POWERX_BROKER_URL", "").rstrip("/")
PRODUCTION_URL = os.getenv("POWERX_PRODUCTION_API_URL", "").rstrip("/")

app = FastAPI(title="PowerX Control API", version="14.0")
started = time.time()

def auth(value):
    if (
        not TOKEN
        or not value
        or not value.startswith("Bearer ")
        or not secrets.compare_digest(value[7:], TOKEN)
    ):
        raise HTTPException(401, "Unauthorized")

async def health(url):
    if not url:
        return {"configured": False, "healthy": False}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url + "/health")
        return {
            "configured": True,
            "healthy": 200 <= r.status_code < 300,
            "status": r.status_code,
            "detail": r.json() if r.headers.get("content-type","").startswith("application/json") else r.text[:500],
        }
    except Exception as exc:
        return {
            "configured": True,
            "healthy": False,
            "error": str(exc),
        }

def capabilities_for(model_id):
    return [
        capability
        for capability, models in CAPABILITY_MODELS.items()
        if model_id in models
    ]

def runtime_for(model_id):
    adapter = MODEL_ADAPTERS[model_id]

    if adapter in {
        "diffusers_sdxl",
        "diffusers_wan",
        "llamacpp_vision",
    }:
        return "gpu16"

    if model_id in {"qwen25-3b-general"}:
        return "mobile/cpu"

    return "cpu/gpu16"

@app.get("/status")
async def status(authorization: str | None = Header(None)):
    auth(authorization)

    cpu = await health(CPU_URL)
    broker = await health(BROKER_URL)
    production = await health(PRODUCTION_URL)

    models = []
    for model_id in MODEL_IDS:
        models.append({
            "id": model_id,
            "name": model_id,
            "adapter": MODEL_ADAPTERS[model_id],
            "capabilities": capabilities_for(model_id),
            "runtime": runtime_for(model_id),
            "registered": True,
        })

    return {
        "ok": True,
        "phase": 14,
        "assistant": "MA",
        "registered_models": len(MODEL_IDS),
        "models": models,
        "runtimes": {
            "modal_cpu": cpu,
            "runtime_broker": broker,
            "production_gateway": production,
            "mobile": {
                "configured": True,
                "note": "Mobile runtime executes on participating Android devices."
            },
            "gpu16": {
                "configured": bool(BROKER_URL),
                "note": "GPU16 workers connect through the runtime broker."
            },
            "beam": {
                "configured": False,
                "optional": True,
            },
        },
    }

@app.get("/health/all")
async def health_all(authorization: str | None = Header(None)):
    auth(authorization)
    return {
        "ok": True,
        "phase": 14,
        "uptime_seconds": int(time.time() - started),
        "registered_models": len(MODEL_IDS),
        "cpu": await health(CPU_URL),
        "broker": await health(BROKER_URL),
        "production": await health(PRODUCTION_URL),
    }

@app.get("/usage")
async def usage(authorization: str | None = Header(None)):
    auth(authorization)
    return {
        "ok": True,
        "uptime_seconds": int(time.time() - started),
        "registered_models": len(MODEL_IDS),
        "runtime_mode": "dynamic",
    }

@app.get("/settings")
def settings(authorization: str | None = Header(None)):
    auth(authorization)
    return {
        "ok": True,
        "phase": 14,
        "assistant": "MA",
        "models": len(MODEL_IDS),
        "automatic_model_routing": True,
        "beam_optional": True,
        "control_token": "configured",
    }

@app.get("/logs")
def logs(authorization: str | None = Header(None)):
    auth(authorization)
    return {"ok": True, "logs": []}

@app.post("/runtime/action")
def runtime_action(authorization: str | None = Header(None)):
    auth(authorization)
    raise HTTPException(
        409,
        "Phase 14 runtimes are automatically controlled by MA orchestration."
    )
