import os
from fastapi import FastAPI, Header, HTTPException
from powerx.agent.schema import AgentRequest
from powerx.agent.config import scheduler_from_env
from powerx.agent.orchestrator import UniversalAgent
app=FastAPI(title="PowerX Universal Agent API",version="1.0.0")
scheduler=scheduler_from_env(); agent=UniversalAgent(scheduler)
@app.get("/health")
async def health():
    return {"ok":True,"service":"powerx-agent","runtimes":[{"id":r.id,"class":r.runtime_class,"model":r.model_id,"capabilities":sorted(r.capabilities)} for r in scheduler.runtimes]}
@app.post("/v1/agent")
async def run_agent(body:AgentRequest,authorization:str|None=Header(default=None)):
    expected=os.getenv("POWERX_AGENT_API_KEY")
    if expected and authorization != f"Bearer {expected}": raise HTTPException(401,"Unauthorized")
    return (await agent.run(body)).model_dump()
