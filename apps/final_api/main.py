import json, time, uuid, os
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from powerx.production.endpoint_config import registry_from_env
from powerx.production.inference import ProductionInferenceCoordinator, NoRuntimeAvailable
from powerx.production.security import APIKeyValidator
from powerx.final.metrics.store import UsageStore
from powerx.final.resources.guard import can_start_work
from powerx.final.resources.queue import ConcurrencyGate
from powerx.final.streaming.openai_sse import stream_chat

app=FastAPI(title="PowerX Final API",version="2.0.0")
registry=registry_from_env()
coordinator=ProductionInferenceCoordinator(registry)
keys=APIKeyValidator()
usage=UsageStore()
gate=ConcurrencyGate(int(os.getenv("POWERX_MAX_CONCURRENT","2")))

class RequestBody(BaseModel):
    task:str
    messages:list[dict]
    max_tokens:int=Field(default=1024,ge=1,le=8192)
    stream:bool=False

@app.on_event("startup")
async def startup():
    os.makedirs("data",exist_ok=True)
    await usage.init()

def authorize(value):
    token=value[7:].strip() if value and value.lower().startswith("bearer ") else None
    if not keys.validate(token): raise HTTPException(401,"Unauthorized")

@app.get("/health")
async def health():
    ok,res=can_start_work()
    return {"ok":True,"resource_ready":ok,"resources":res}

@app.get("/usage")
async def usage_summary(authorization:str|None=Header(None)):
    authorize(authorization); return await usage.summary()

@app.post("/v2/inference")
async def infer(body:RequestBody,authorization:str|None=Header(None)):
    authorize(authorization)
    resource_ok,res=can_start_work()
    if not resource_ok: raise HTTPException(503,{"error":"Resource guard blocked new work","resources":res})
    request_id=str(uuid.uuid4()); t=time.perf_counter()

    async with gate.slot():
        if body.stream:
            try:
                target=await coordinator.resolve(body.task)
            except NoRuntimeAvailable as e:
                raise HTTPException(503,str(e))
            payload={"model":target.model_id,"messages":body.messages,"max_tokens":body.max_tokens}
            async def gen():
                total=""
                try:
                    async for chunk in stream_chat(target.base_url,target.api_key,payload):
                        total+=chunk
                        yield f"data: {json.dumps({'request_id':request_id,'delta':chunk})}\n\n"
                    latency=int((time.perf_counter()-t)*1000)
                    await usage.record(request_id=request_id,task=body.task,model_id=target.model_id,runtime=target.runtime_class,latency_ms=latency,ok=True,input_chars=sum(len(str(m.get('content',''))) for m in body.messages),output_chars=len(total))
                    yield "data: [DONE]\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({'error':str(e)})}\n\n"
            return StreamingResponse(gen(),media_type="text/event-stream")

        try:
            result=await coordinator.chat(task=body.task,messages=body.messages,max_tokens=body.max_tokens)
            latency=int((time.perf_counter()-t)*1000)
            text=""
            try:text=result.response.get("choices",[{}])[0].get("message",{}).get("content","")
            except Exception:pass
            await usage.record(request_id=request_id,task=body.task,model_id=result.model_id,runtime=result.runtime_class,latency_ms=latency,ok=True,input_chars=sum(len(str(m.get('content',''))) for m in body.messages),output_chars=len(text))
            return {"ok":True,"request_id":request_id,"model_id":result.model_id,"runtime":result.runtime_class,"text":text,"raw":result.response}
        except Exception as e:
            latency=int((time.perf_counter()-t)*1000)
            await usage.record(request_id=request_id,task=body.task,model_id=None,runtime=None,latency_ms=latency,ok=False)
            raise HTTPException(503,str(e))
