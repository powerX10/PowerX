"""PowerX Phase 12 control API with durable pull-worker broker."""
from __future__ import annotations

import os
from fastapi import FastAPI, Header, HTTPException, Query

from powerx.runtime_fabric.broker import JobBroker
from powerx.runtime_fabric.config import load_fabric_config
from powerx.runtime_fabric.scheduler import FabricScheduler, TaskIntent
from powerx.runtime_fabric.health import check_node
from powerx.runtime_fabric.gateway import RuntimeFabricGateway, NoFabricNode

app = FastAPI(title="PowerX Runtime Fabric", version="12.1")
config = load_fabric_config()
scheduler = FabricScheduler(config)
gateway = RuntimeFabricGateway(scheduler)
broker = JobBroker()


def _worker_auth(authorization: str | None):
    expected = os.getenv("POWERX_WORKER_TOKEN", "")
    if not expected:
        return
    if authorization != f"Bearer {expected}":
        raise HTTPException(status_code=401, detail="unauthorized")


@app.get("/health")
def health():
    return {
        "ok": True,
        "phase": 12,
        "nodes": [check_node(n).__dict__ for n in config.nodes],
    }


@app.post("/route")
def route(body: dict):
    task = TaskIntent(
        capability=str(body.get("capability", "chat")),
        size=str(body.get("size", "normal")),
        user_device_available=bool(body.get("user_device_available", False)),
        requires_gpu=bool(body.get("requires_gpu", False)),
    )
    return {
        "runtime_order": scheduler.runtime_order(task),
        "nodes": [n.id for n in scheduler.candidates(task)],
    }


@app.post("/infer")
def infer(body: dict):
    task = TaskIntent(
        capability=str(body.get("capability", "chat")),
        size=str(body.get("size", "normal")),
        user_device_available=bool(body.get("user_device_available", False)),
        requires_gpu=bool(body.get("requires_gpu", False)),
    )
    try:
        return gateway.infer(task, dict(body.get("payload", {})))
    except NoFabricNode as exc:
        raise HTTPException(status_code=503, detail=exc.args[0])


@app.post("/workers/jobs")
def create_worker_job(
    body: dict,
    authorization: str | None = Header(default=None),
):
    _worker_auth(authorization)
    runtime_class = str(body.get("runtime_class") or "")
    capability = str(body.get("capability") or "")
    payload = body.get("payload") or {}

    if runtime_class not in {"gpu16", "mobile"}:
        raise HTTPException(422, "runtime_class must be gpu16 or mobile")
    if not capability:
        raise HTTPException(422, "capability required")
    if not isinstance(payload, dict):
        raise HTTPException(422, "payload must be an object")

    job = broker.submit(runtime_class, capability, payload)
    return {"ok": True, "job": job.__dict__}


@app.get("/workers/pull")
def pull_worker_job(
    runtime_class: str = Query(...),
    authorization: str | None = Header(default=None),
):
    _worker_auth(authorization)
    if runtime_class not in {"gpu16", "mobile"}:
        raise HTTPException(422, "unsupported runtime_class")
    job = broker.pull(runtime_class)
    return {"ok": True, "job": job.__dict__ if job else None}


@app.post("/workers/result")
def worker_result(
    body: dict,
    authorization: str | None = Header(default=None),
):
    _worker_auth(authorization)
    job_id = str(body.get("job_id") or "")
    if not job_id:
        raise HTTPException(422, "job_id required")
    try:
        job = broker.complete(
            job_id,
            ok=bool(body.get("ok", False)),
            result=body.get("result"),
            error=body.get("error"),
        )
    except KeyError:
        raise HTTPException(404, "job not found")
    return {"ok": True, "job": job.__dict__}


@app.get("/workers/jobs/{job_id}")
def get_worker_job(
    job_id: str,
    authorization: str | None = Header(default=None),
):
    _worker_auth(authorization)
    try:
        job = broker.get(job_id)
    except KeyError:
        raise HTTPException(404, "job not found")
    return {"ok": True, "job": job.__dict__}
