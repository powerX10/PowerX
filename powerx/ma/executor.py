import asyncio,os,time,httpx
class RuntimeExecutor:
    async def direct(self,tok,url,mid,cap,payload):
        h={"Content-Type":"application/json"}
        if tok:h["Authorization"]=f"Bearer {tok}"
        async with httpx.AsyncClient(timeout=float(os.getenv("POWERX_INFERENCE_TIMEOUT","900"))) as c:
            r=await c.post(url.rstrip("/")+"/infer",headers=h,json={"model_id":mid,"capability":cap,"payload":payload})
        r.raise_for_status();return r.json()
    async def broker(self,tok,url,rt,mid,cap,payload):
        h={"Content-Type":"application/json"}
        if tok:h["Authorization"]=f"Bearer {tok}"
        async with httpx.AsyncClient(timeout=60) as c:
            r=await c.post(url.rstrip("/")+"/workers/jobs",headers=h,json={"runtime_class":rt,"capability":cap,"payload":{"model_id":mid,**payload}})
            r.raise_for_status();j=r.json()["job"];end=time.time()+float(os.getenv("POWERX_JOB_TIMEOUT","1200"))
            while time.time()<end:
                q=await c.get(url.rstrip("/")+f"/workers/jobs/{j['id']}",headers=h);q.raise_for_status();s=q.json()["job"]
                if s["status"]=="completed":return s.get("result") or {}
                if s["status"]=="failed":raise RuntimeError(s.get("error") or "worker_failed")
                await asyncio.sleep(2)
        raise TimeoutError(j["id"])
