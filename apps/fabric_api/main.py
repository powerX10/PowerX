from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from powerx.fabric.schema import RuntimeNode
from powerx.fabric.registry import RuntimeFabricRegistry
from powerx.fabric.router import RuntimeFabricRouter
from powerx.fabric.policy import TaskProfile
from powerx.fabric.escalation import classify

app=FastAPI(title="PowerX Runtime Fabric API",version="1.0.0")
registry=RuntimeFabricRegistry()
router=RuntimeFabricRouter(registry)

class Heartbeat(BaseModel):
    id:str; runtime_class:str; base_url:str
    capabilities:list[str]; model_tiers:list[str]
    always_on:bool=False; available:bool=True
    load:float=Field(default=0.0,ge=0.0,le=1.0)
    ram_gb:float=0.0; vram_gb:float=0.0; metadata:dict={}

class ResolveRequest(BaseModel):
    capability:str
    prompt_chars:int=0
    requested_tier:str|None=None
    device_local:bool=False
    continuous:bool=False

@app.get("/health")
async def health():
    return {"ok":True,"service":"powerx-fabric","nodes":registry.snapshot()}

@app.post("/v1/nodes/heartbeat")
async def heartbeat(body:Heartbeat):
    if body.runtime_class not in {"cpu","mobile","gpu16","cloud"}:
        raise HTTPException(422,"Unsupported runtime class")
    registry.heartbeat(RuntimeNode(
        body.id,body.runtime_class,body.base_url,set(body.capabilities),set(body.model_tiers),
        body.always_on,body.available,body.load,body.ram_gb,body.vram_gb,body.metadata
    ))
    return {"ok":True}

@app.post("/v1/resolve")
async def resolve(body:ResolveRequest):
    e=classify(body.capability,body.prompt_chars,body.requested_tier)
    try:
        n=router.resolve(TaskProfile(body.capability,e.requested_tier,e.heavy,body.device_local,body.continuous))
    except RuntimeError as ex:
        raise HTTPException(503,str(ex))
    return {"ok":True,"runtime":{**n.__dict__,"capabilities":sorted(n.capabilities),"model_tiers":sorted(n.model_tiers)},"escalation":e.__dict__}
