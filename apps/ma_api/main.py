import os,secrets
from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel,Field
from powerx.ma import MAOrchestrator,MARequest,Attachment
app=FastAPI(title="PowerX MA",version="13");ma=MAOrchestrator()
class A(BaseModel):name:str;mime_type:str;data_b64:str|None=None;url:str|None=None
class B(BaseModel):
    text:str="";messages:list[dict]=Field(default_factory=list);attachments:list[A]=Field(default_factory=list)
    product_id:str="powerx";user_id:str|None=None;founder_mode:bool=False;preferred_runtime:str|None=None;metadata:dict=Field(default_factory=dict)
def auth(v):
    k=os.getenv("POWERX_PRODUCTION_API_KEY","")
    if k and (not v or not v.startswith("Bearer ") or not secrets.compare_digest(v[7:],k)):raise HTTPException(401)
@app.get("/health")
def health():return {"ok":True,"phase":13}
@app.post("/v1/ma")
async def run(b:B,authorization:str|None=Header(None)):
    auth(authorization);r=MARequest(b.text,b.messages,[Attachment(**x.model_dump()) for x in b.attachments],b.product_id,b.user_id,b.founder_mode,b.preferred_runtime,b.metadata)
    return (await ma.run(r)).__dict__
@app.post("/v1/chat")
async def chat(b:B,authorization:str|None=Header(None)):return await run(b,authorization)
