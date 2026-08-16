from __future__ import annotations
import os, secrets
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from powerx.final_runtime.registry_sync import FinalRegistrySync
from powerx.final_runtime.readiness import FinalReadinessAudit
from powerx.final_runtime.unified import UnifiedPowerX
from powerx.trading.roles import TradingRoleRegistry
from powerx.trading.provider import CMSModelProvider, OpenAICompatibleRuntime
from powerx.trading.orchestrator import TradingSwarmOrchestrator
from powerx.trading.schema import TradingRequest

TOKEN = os.getenv("POWERX_CONTROL_TOKEN", "")
app = FastAPI(title="PowerX Final Unified API", version="11.0.0")
unified = UnifiedPowerX()

def auth(value: str | None):
    if not TOKEN or not value or not value.startswith("Bearer ") or not secrets.compare_digest(value[7:], TOKEN):
        raise HTTPException(401, "Unauthorized")

class ChatBody(BaseModel):
    messages: list[dict]
    capability: str = "chat"
    max_tokens: int = Field(default=900, ge=1, le=8192)
    preferred_runtime: str | None = None

class PromptBody(BaseModel):
    prompt: str
    options: dict = Field(default_factory=dict)

class SpeechBody(BaseModel):
    audio_ref: str
    options: dict = Field(default_factory=dict)

class TTSBody(BaseModel):
    text: str
    options: dict = Field(default_factory=dict)

@app.get("/health")
async def health():
    return {"ok":True,"service":"powerx-final-api","version":11}

@app.post("/v1/admin/sync-registry")
async def sync_registry(authorization: str | None = Header(None)):
    auth(authorization)
    return FinalRegistrySync().sync(preserve_existing_runtime_overrides=True)

@app.get("/v1/admin/readiness")
async def readiness(check_endpoints: bool = False, authorization: str | None = Header(None)):
    auth(authorization)
    return await FinalReadinessAudit().run(check_endpoints=check_endpoints)

@app.post("/v1/chat")
async def chat(body: ChatBody, authorization: str | None = Header(None)):
    auth(authorization)
    return await unified.chat(body.messages, body.capability, body.max_tokens, body.preferred_runtime)

@app.post("/v1/image")
async def image(body: PromptBody, authorization: str | None = Header(None)):
    auth(authorization)
    return await unified.image(body.prompt, **body.options)

@app.post("/v1/video")
async def video(body: PromptBody, authorization: str | None = Header(None)):
    auth(authorization)
    return await unified.video(body.prompt, **body.options)

@app.post("/v1/stt")
async def stt(body: SpeechBody, authorization: str | None = Header(None)):
    auth(authorization)
    return await unified.transcribe(body.audio_ref, **body.options)

@app.post("/v1/tts")
async def tts(body: TTSBody, authorization: str | None = Header(None)):
    auth(authorization)
    return await unified.speak(body.text, **body.options)

@app.post("/v1/trading/analyze")
async def trading(body: TradingRequest, authorization: str | None = Header(None)):
    auth(authorization)
    roles = TradingRoleRegistry()
    swarm = TradingSwarmOrchestrator(roles, CMSModelProvider(), OpenAICompatibleRuntime())
    return (await swarm.run(body)).model_dump(mode="json")
