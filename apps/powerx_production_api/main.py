from __future__ import annotations

import os
import secrets
import httpx
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from powerx.runtime_fabric.chat_bridge import chat_payload

app = FastAPI(title="PowerX Production Gateway", version="12.2")

API_KEY = os.getenv("POWERX_PRODUCTION_API_KEY") or os.getenv("POWERX_WORKER_TOKEN", "")
CPU_URL = os.getenv("POWERX_MODAL_CPU_URL", "").rstrip("/")
CPU_TOKEN = os.getenv("POWERX_MODAL_CPU_TOKEN") or os.getenv("POWERX_WORKER_TOKEN", "")
BROKER_URL = os.getenv("POWERX_BROKER_URL", "").rstrip("/")
DEFAULT_CHAT_MODEL = os.getenv("POWERX_DEFAULT_CHAT_MODEL", "qwen25-3b-general")


def _auth(value: str | None) -> None:
    if not API_KEY:
        raise HTTPException(503, "POWERX_PRODUCTION_API_KEY is not configured")
    if not value or not value.startswith("Bearer "):
        raise HTTPException(401, "Unauthorized")
    if not secrets.compare_digest(value[7:], API_KEY):
        raise HTTPException(401, "Unauthorized")


class ChatBody(BaseModel):
    messages: list[dict] | None = None
    message: str | None = None
    prompt: str | None = None
    text: str | None = None
    capability: str = "chat"
    model_id: str | None = None
    max_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)


class MobileJobBody(BaseModel):
    capability: str = "chat"
    payload: dict = Field(default_factory=dict)


@app.get("/health")
async def health():
    cpu = {"configured": bool(CPU_URL), "healthy": False}
    if CPU_URL:
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.get(CPU_URL + "/health")
            cpu = {"configured": True, "healthy": r.status_code < 500, "status": r.status_code}
        except Exception as exc:
            cpu = {"configured": True, "healthy": False, "error": str(exc)}
    return {
        "ok": True,
        "service": "powerx-production-gateway",
        "cpu": cpu,
        "broker_configured": bool(BROKER_URL),
        "default_chat_model": DEFAULT_CHAT_MODEL,
    }


async def _cpu_chat(body: dict):
    if not CPU_URL:
        raise HTTPException(503, "POWERX_MODAL_CPU_URL is not configured")
    payload = chat_payload(body)
    model_id = str(body.get("model_id") or DEFAULT_CHAT_MODEL)
    headers = {"Content-Type": "application/json"}
    if CPU_TOKEN:
        headers["Authorization"] = f"Bearer {CPU_TOKEN}"

    request_body = {
        "model_id": model_id,
        "capability": str(body.get("capability") or "chat"),
        "payload": payload,
    }
    try:
        async with httpx.AsyncClient(timeout=float(os.getenv("POWERX_INFERENCE_TIMEOUT", "300"))) as c:
            r = await c.post(CPU_URL + "/infer", headers=headers, json=request_body)
        r.raise_for_status()
        data = r.json()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:2000]
        raise HTTPException(exc.response.status_code, detail)
    except Exception as exc:
        raise HTTPException(503, f"CPU inference unavailable: {exc}")

    # Normalize Modal worker result for the existing PowerX Chat UI.
    result = data.get("result", data) if isinstance(data, dict) else data
    text = None
    if isinstance(result, dict):
        choices = result.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                msg = first.get("message")
                if isinstance(msg, dict):
                    text = msg.get("content")
                if text is None:
                    text = first.get("text")
        if text is None and isinstance(result.get("text"), str):
            text = result["text"]

    return {
        "ok": True,
        "provider": "modal",
        "runtime_class": "cpu",
        "model_id": model_id,
        "message": text,
        "result": result,
    }


@app.post("/v1/chat")
async def chat(body: ChatBody, authorization: str | None = Header(None)):
    _auth(authorization)
    return await _cpu_chat(body.model_dump(exclude_none=True))


# Backward compatibility with older control-center builds.
@app.post("/v1/inference/chat")
async def chat_compat(body: ChatBody, authorization: str | None = Header(None)):
    _auth(authorization)
    return await _cpu_chat(body.model_dump(exclude_none=True))


@app.post("/v1/mobile/jobs")
async def create_mobile_job(body: MobileJobBody, authorization: str | None = Header(None)):
    _auth(authorization)
    if not BROKER_URL:
        raise HTTPException(503, "POWERX_BROKER_URL is not configured")
    headers = {"Content-Type": "application/json"}
    if CPU_TOKEN:
        headers["Authorization"] = f"Bearer {CPU_TOKEN}"
    payload = {
        "runtime_class": "mobile",
        "capability": body.capability,
        "payload": body.payload,
    }
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(BROKER_URL + "/workers/jobs", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()


@app.get("/v1/mobile/jobs/{job_id}")
async def get_mobile_job(job_id: str, authorization: str | None = Header(None)):
    _auth(authorization)
    if not BROKER_URL:
        raise HTTPException(503, "POWERX_BROKER_URL is not configured")
    headers = {}
    if CPU_TOKEN:
        headers["Authorization"] = f"Bearer {CPU_TOKEN}"
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.get(BROKER_URL + f"/workers/jobs/{job_id}", headers=headers)
    r.raise_for_status()
    return r.json()
