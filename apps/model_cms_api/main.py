from __future__ import annotations
import os, secrets
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from powerx.controlplane.models import ManagedModel
from powerx.controlplane.store import ControlPlaneStore
from powerx.controlplane.resolver import DynamicRuntimeResolver
from powerx.controlplane.runtime_config import build_launch_config

TOKEN = os.getenv("POWERX_CONTROL_TOKEN", "")
store = ControlPlaneStore()
resolver = DynamicRuntimeResolver(store)
app = FastAPI(title="PowerX Model CMS API", version="2.0")

def auth(value: str | None):
    if not TOKEN or not value or not value.startswith("Bearer ") or not secrets.compare_digest(value[7:], TOKEN):
        raise HTTPException(401, "Unauthorized")

class PatchBody(BaseModel):
    patch: dict

class ResolveBody(BaseModel):
    capability: str
    preferred_runtime: str | None = None

@app.get("/health")
def health():
    return {"ok": True, "service": "powerx-model-cms", "models": len(store.list())}

@app.get("/v1/models")
def models(authorization: str | None = Header(None)):
    auth(authorization)
    return {"models": [m.model_dump(mode="json") for m in store.list()]}

@app.get("/v1/models/{model_id}")
def model(model_id: str, authorization: str | None = Header(None)):
    auth(authorization)
    try:
        return store.get(model_id).model_dump(mode="json")
    except KeyError:
        raise HTTPException(404, "Model not found")

@app.put("/v1/models/{model_id}")
def put_model(model_id: str, body: ManagedModel, authorization: str | None = Header(None)):
    auth(authorization)
    if body.id != model_id:
        raise HTTPException(422, "Path id and body id must match")
    return store.upsert(body).model_dump(mode="json")

@app.patch("/v1/models/{model_id}")
def patch_model(model_id: str, body: PatchBody, authorization: str | None = Header(None)):
    auth(authorization)
    try:
        return store.patch(model_id, body.patch).model_dump(mode="json")
    except KeyError:
        raise HTTPException(404, "Model not found")

@app.delete("/v1/models/{model_id}")
def delete_model(model_id: str, authorization: str | None = Header(None)):
    auth(authorization)
    return {"ok": store.delete(model_id)}

@app.post("/v1/resolve")
def resolve(body: ResolveBody, authorization: str | None = Header(None)):
    auth(authorization)
    return {"candidates": [x.__dict__ for x in resolver.candidates(body.capability, body.preferred_runtime)]}

@app.get("/v1/models/{model_id}/launch/{runtime_class}")
def launch_config(model_id: str, runtime_class: str, authorization: str | None = Header(None)):
    auth(authorization)
    try:
        return build_launch_config(store.get(model_id), runtime_class).__dict__
    except KeyError as exc:
        raise HTTPException(404, str(exc))

@app.get("/cms", response_class=HTMLResponse)
def cms():
    return HTMLResponse('''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>PowerX Model CMS</title><style>body{font-family:system-ui;background:#0b0d10;color:#eee;margin:24px}input,select,button,textarea{background:#171b21;color:#fff;border:1px solid #333;border-radius:8px;padding:9px}table{width:100%;border-collapse:collapse;margin-top:18px}td,th{padding:8px;border-bottom:1px solid #262b32;text-align:left}.pill{padding:3px 7px;border-radius:20px;background:#222}button{cursor:pointer}.row{display:flex;gap:8px;flex-wrap:wrap}</style></head><body><h1>PowerX Model CMS</h1><p>CPU/GPU/mobile/cloud routing is runtime-configurable, not hardcoded.</p><div class="row"><input id="token" type="password" placeholder="POWERX_CONTROL_TOKEN"><button onclick="load()">Load</button></div><div id="app"></div><script>
async function api(path,init={}){const t=document.getElementById('token').value;const r=await fetch(path,{...init,headers:{'Content-Type':'application/json','Authorization':'Bearer '+t,...(init.headers||{})}});return r.json()}
async function load(){const d=await api('/v1/models');let h='<table><tr><th>Model</th><th>Capabilities</th><th>Enabled</th><th>Runtime bindings</th></tr>';for(const m of d.models||[]){h+=`<tr><td><b>${m.display_name}</b><br><small>${m.id}</small></td><td>${m.capabilities.map(x=>`<span class=pill>${x}</span>`).join(' ')}</td><td><button onclick="toggle('${m.id}',${!m.enabled})">${m.enabled?'ON':'OFF'}</button></td><td>${m.bindings.map(b=>`${b.runtime_class}:${b.enabled?'ON':'OFF'} p${b.priority}`).join('<br>')}</td></tr>`}document.getElementById('app').innerHTML=h+'</table>'}
async function toggle(id,val){await api('/v1/models/'+id,{method:'PATCH',body:JSON.stringify({patch:{enabled:val}})});load()}
</script></body></html>''')
