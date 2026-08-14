import httpx

class FinalPowerXClient:
    def __init__(self,base_url:str,api_key:str,timeout:float=180):
        self.base_url=base_url.rstrip("/");self.api_key=api_key;self.timeout=timeout
    async def infer(self,task:str,messages:list[dict],max_tokens:int=1024):
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            r=await c.post(self.base_url+"/v2/inference",headers={"Authorization":f"Bearer {self.api_key}"},json={"task":task,"messages":messages,"max_tokens":max_tokens,"stream":False})
            r.raise_for_status();return r.json()
