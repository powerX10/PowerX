import os,httpx
class PowerXClient:
    def __init__(self,base_url=None,api_key=None,product_id="powerx"):
        self.base_url=(base_url or os.getenv("POWERX_PRODUCTION_API_URL","")).rstrip("/")
        self.api_key=api_key or os.getenv("POWERX_PRODUCTION_API_KEY","");self.product_id=product_id
    async def ask(self,text="",messages=None,attachments=None,founder_mode=False,metadata=None):
        if not self.base_url:raise RuntimeError("POWERX_PRODUCTION_API_URL missing")
        h={"Content-Type":"application/json"}
        if self.api_key:h["Authorization"]=f"Bearer {self.api_key}"
        async with httpx.AsyncClient(timeout=float(os.getenv("POWERX_INFERENCE_TIMEOUT","1200"))) as c:
            r=await c.post(self.base_url+"/v1/ma",headers=h,json={"text":text,"messages":messages or [],
             "attachments":attachments or [],"product_id":self.product_id,"founder_mode":founder_mode,"metadata":metadata or {}})
        r.raise_for_status();return r.json()
