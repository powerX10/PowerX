from fastapi import FastAPI
from powerx.core.orchestrator import PowerXOrchestrator
from powerx.models.catalog import list_models
from powerx.router.router import route_task
from powerx.router.task_types import TaskType
from apps.api.schemas import ChatRequest

app = FastAPI(
    title="PowerX Core API",
    version="0.1.0",
    description="Central AI-model orchestration API.",
)

orchestrator = PowerXOrchestrator()


@app.get("/health")
async def health():
    return {"ok": True, "service": "powerx", "phase": 1}


@app.get("/v1/models")
async def models():
    return [m.__dict__ for m in list_models()]


@app.get("/v1/route/{task}")
async def route(task: TaskType):
    return route_task(task).__dict__


@app.post("/v1/chat")
async def chat(req: ChatRequest):
    return await orchestrator.execute_chat(
        task=req.task,
        messages=req.messages,
        max_tokens=req.max_tokens,
    )
