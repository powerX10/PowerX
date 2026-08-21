from __future__ import annotations
import os, secrets, traceback
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from powerx.v2.schema import ModelSpec
from powerx.v2.model_manager import ModelManager
from powerx.v2.resource_probe import probe

app=FastAPI(title="PowerX V2 Lightning Worker",version="2.0-zip2")
manager=ModelManager()

class RunBody(BaseModel):
    model: dict
    request: dict
    capability: str

def auth(value:str|None):
    token=os.getenv("POWERX_LIGHTNING_WORKER_TOKEN","")
    if not token: return
    if not value or not value.startswith("Bearer ") or not secrets.compare_digest(value[7:],token):
        raise HTTPException(401,"Invalid worker token")

@app.get("/health")
def health():
    return {"ok":True,"version":"2.0-zip2","resources":probe(os.getenv("POWERX_CACHE_ROOT",".")).as_dict(),"loaded_models":list(manager.loaded.keys())}

@app.post("/v1/run")
def run(body:RunBody,authorization:str|None=Header(None)):
    auth(authorization)
    try:
        spec=ModelSpec.model_validate(body.model)
        result=manager.run(spec,{"request":body.request,"capability":body.capability})
        return {"ok":True,**result}
    except Exception as e:
        return {"ok":False,"errors":[f"{type(e).__name__}: {e}"],"trace":traceback.format_exc() if os.getenv("POWERX_DEBUG","0")=="1" else None}

@app.post("/v1/unload")
def unload(model_id:str|None=None,authorization:str|None=Header(None)):
    auth(authorization)
    return {"ok":True,"unloaded":manager.unload(model_id)}


# PowerX V2 ZIP3 routes
from apps.lightning_worker.media_routes import router as media_router
from apps.lightning_worker.forecast_routes import router as forecast_router
app.include_router(media_router)
app.include_router(forecast_router)
