import os

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

from powerx.production.audit import JSONLAuditLogger
from powerx.production.endpoint_config import registry_from_env
from powerx.production.inference import (
    NoRuntimeAvailable,
    ProductionInferenceCoordinator,
)
from powerx.production.readiness import run_preflight
from powerx.production.request_context import RequestContext
from powerx.production.security import APIKeyValidator, SlidingWindowRateLimiter
from powerx.production.validation import validate_messages


class ProductionChatRequest(BaseModel):
    task: str
    messages: list[dict]
    max_tokens: int = Field(default=1024, ge=1, le=8192)


app = FastAPI(title="PowerX Production API", version="1.0.0")
registry = registry_from_env()
coordinator = ProductionInferenceCoordinator(registry)
keys = APIKeyValidator()
limiter = SlidingWindowRateLimiter(
    requests=int(os.getenv("POWERX_RATE_LIMIT", "60")),
    window_seconds=60,
)
audit = JSONLAuditLogger(os.getenv("POWERX_AUDIT_LOG", "logs/powerx-audit.jsonl"))


@app.get("/health")
async def health():
    return {"ok": True, "service": "powerx-production"}


@app.get("/ready")
async def ready():
    return run_preflight()


@app.post("/v1/inference/chat")
async def inference_chat(
    body: ProductionChatRequest,
    request: Request,
    authorization: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None),
):
    ctx = RequestContext.create(x_request_id)

    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()

    if not keys.validate(token):
        audit.write("auth_failed", request_id=ctx.request_id)
        raise HTTPException(status_code=401, detail="Unauthorized")

    identity = request.client.host if request.client else "unknown"
    if not limiter.allow(identity):
        audit.write("rate_limited", request_id=ctx.request_id, identity=identity)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    try:
        validate_messages(body.messages)
        result = await coordinator.chat(
            task=body.task,
            messages=body.messages,
            max_tokens=body.max_tokens,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except NoRuntimeAvailable as exc:
        audit.write(
            "runtime_unavailable",
            request_id=ctx.request_id,
            task=body.task,
            error=str(exc),
        )
        raise HTTPException(status_code=503, detail=str(exc))

    audit.write(
        "inference_ok",
        request_id=ctx.request_id,
        task=body.task,
        model_id=result.model_id,
        runtime_id=result.runtime_id,
        runtime_class=result.runtime_class,
    )

    return {
        "request_id": ctx.request_id,
        "ok": True,
        "model_id": result.model_id,
        "runtime": result.runtime_class,
        "output": result.response,
    }
