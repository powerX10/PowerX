from __future__ import annotations
import os, secrets
from fastapi import FastAPI, Header, HTTPException
from powerx.trading.schema import TradingRequest
from powerx.trading.roles import TradingRoleRegistry
from powerx.trading.provider import CMSModelProvider, OpenAICompatibleRuntime
from powerx.trading.orchestrator import TradingSwarmOrchestrator

TOKEN = os.getenv("POWERX_API_KEY", "")
app = FastAPI(title="PowerX Trading Intelligence API", version="1.0")
roles = TradingRoleRegistry()
orchestrator = TradingSwarmOrchestrator(roles, CMSModelProvider(), OpenAICompatibleRuntime())

def auth(value):
    if not TOKEN or not value or not value.startswith("Bearer ") or not secrets.compare_digest(value[7:], TOKEN):
        raise HTTPException(401, "Unauthorized")

@app.get("/health")
def health():
    return {"ok":True,"service":"powerx-trading","specialists":len(roles.all())}

@app.get("/v1/trading/roles")
def list_roles(authorization: str | None = Header(None)):
    auth(authorization)
    return {"roles":[r.__dict__ for r in roles.all()]}

@app.post("/v1/trading/analyze")
async def analyze(body: TradingRequest, authorization: str | None = Header(None)):
    auth(authorization)
    return (await orchestrator.run(body)).model_dump(mode="json")
