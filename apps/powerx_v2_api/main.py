from __future__ import annotations
import secrets
from fastapi import FastAPI, Header, HTTPException
from powerx.v2.settings import PowerXSettings
from powerx.v2.registry import ModelRegistry
from powerx.v2.runtime import RuntimeBroker
from powerx.v2.jobs import JobQueue
from powerx.v2.schema import PowerXRequest

app = FastAPI(title="PowerX V2 API", version="2.0-zip1")
settings = PowerXSettings.load()
registry = ModelRegistry()
broker = RuntimeBroker()
queue = JobQueue()

def auth(authorization: str | None):
    if not settings.api_key:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing bearer token")
    if not secrets.compare_digest(authorization[7:], settings.api_key):
        raise HTTPException(401, "Invalid bearer token")

@app.get("/health")
def health():
    return {"ok": True, "version": "2.0-zip1", "mock_mode": settings.mock_mode, "registry": str(settings.registry_path)}

@app.get("/v1/models")
def models(authorization: str | None = Header(None)):
    auth(authorization)
    return {"models": [m.model_dump() for m in registry.all()]}

@app.post("/v1/run")
async def run(req: PowerXRequest, authorization: str | None = Header(None)):
    auth(authorization)
    return await broker.run(req)

@app.post("/v1/jobs")
def submit(req: PowerXRequest, authorization: str | None = Header(None)):
    auth(authorization)
    job = queue.submit(req)
    return {"job_id": job.id, "status": job.status}

@app.get("/v1/jobs/{job_id}")
def job_status(job_id: str, authorization: str | None = Header(None)):
    auth(authorization)
    job = queue.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return {"job_id": job.id, "status": job.status, "result": job.result.model_dump() if job.result else None, "error": job.error}
