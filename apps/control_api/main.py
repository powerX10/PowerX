from pathlib import Path
import os, time, json, secrets
from fastapi import FastAPI, Header, HTTPException, UploadFile, File
from pydantic import BaseModel
import psutil

from powerx.models.catalog import list_models
from powerx.runtime.gpu.capabilities import GPUCapabilityDetector
from powerx.runtime.gpu.controller import GPURuntimeController
from powerx.runtime_cpu.llamacpp.controller import CPURuntimeController
from powerx.runtime_cpu.llamacpp.profiles import CPU_PROFILES

TOKEN=os.getenv("POWERX_CONTROL_TOKEN","")
UPLOAD=Path(os.getenv("POWERX_UPLOAD_DIR","data/uploads"));UPLOAD.mkdir(parents=True,exist_ok=True)
app=FastAPI(title="PowerX Control API",version="1.0")
gpu=GPURuntimeController();cpu=CPURuntimeController();started=time.time()

def auth(value):
    if not TOKEN or not value or not value.startswith("Bearer ") or not secrets.compare_digest(value[7:],TOKEN):
        raise HTTPException(401,"Unauthorized")

class Action(BaseModel):
    action:str
    model_id:str

@app.get("/status")
def status(authorization:str|None=Header(None)):
    auth(authorization)
    models=[]
    for m in list_models():
        s={"id":m.id,"name":m.display_name,"role":m.capability,"runtime":m.preferred_runtime,"healthy":False}
        try:
            if m.preferred_runtime=="gpu16": s["healthy"]=bool(gpu.status(m.id).get("running"))
            elif m.preferred_runtime=="cpu": s["healthy"]=bool(cpu.status(m.id).get("running"))
        except Exception: pass
        models.append(s)
    g=GPUCapabilityDetector.summary()
    return {"gpu":{"running":sum(1 for m in models if m["runtime"]=="gpu16" and m["healthy"]),"detail":g},"cpu":{"running":sum(1 for m in models if m["runtime"]=="cpu" and m["healthy"])},"mobile":{"running":0,"detail":"Mobile endpoint health is resolved by production runtime registry."},"models":models}

@app.post("/runtime/action")
def runtime_action(body:Action,authorization:str|None=Header(None)):
    auth(authorization)
    if body.action not in {"start","stop","status"}: raise HTTPException(422,"Invalid action")
    if body.model_id in {"gpt-oss-20b","qwen-8b","vision-4b"}:
        return getattr(gpu,body.action)(body.model_id)
    if body.model_id in CPU_PROFILES:
        return getattr(cpu,body.action)(body.model_id)
    raise HTTPException(404,"Runtime profile not found")

@app.get("/health/all")
def health(authorization:str|None=Header(None)):
    auth(authorization)
    return {"ok":True,"uptime_seconds":int(time.time()-started),"cpu_percent":psutil.cpu_percent(),"memory":psutil.virtual_memory()._asdict(),"gpu":GPUCapabilityDetector.summary()}

@app.get("/usage")
def usage(authorization:str|None=Header(None)):
    auth(authorization)
    p=psutil.Process()
    return {"process":{"rss_mb":round(p.memory_info().rss/1024/1024,2),"cpu_percent":p.cpu_percent()},"system":{"cpu_percent":psutil.cpu_percent(),"memory_percent":psutil.virtual_memory().percent},"uptime_seconds":int(time.time()-started)}

@app.get("/settings")
def settings(authorization:str|None=Header(None)):
    auth(authorization)
    return {"control_token":"configured" if TOKEN else "missing","upload_dir":str(UPLOAD),"production_api":"configured" if os.getenv("POWERX_API_KEY") else "check production API environment","owner":"single-owner UI"}

@app.get("/logs")
def logs(authorization:str|None=Header(None)):
    auth(authorization)
    out=[]
    for folder in [Path(".powerx-runtime"),Path(".powerx-cpu-runtime"),Path("logs")]:
        if folder.exists():
            for p in folder.glob("*.log*"):
                try: out.append({"file":str(p),"tail":"\n".join(p.read_text(errors="ignore").splitlines()[-80:])})
                except Exception: pass
    return {"logs":out[-20:]}

@app.post("/files")
async def files(file:UploadFile=File(...),authorization:str|None=Header(None)):
    auth(authorization)
    safe=Path(file.filename or "upload.bin").name
    target=UPLOAD/f"{int(time.time())}-{safe}"
    size=0
    with target.open("wb") as f:
        while chunk:=await file.read(1024*1024):
            size+=len(chunk)
            if size>25*1024*1024:
                target.unlink(missing_ok=True);raise HTTPException(413,"25MB limit")
            f.write(chunk)
    return {"ok":True,"name":safe,"path":str(target),"size":size}
