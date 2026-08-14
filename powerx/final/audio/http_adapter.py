import httpx
from powerx.final.audio.base import STTProvider, TTSProvider

class HTTPSTT(STTProvider):
    def __init__(self, base_url: str, token: str | None = None):
        self.base_url=base_url.rstrip("/"); self.token=token
    async def transcribe(self,audio_path:str)->dict:
        headers={}
        if self.token: headers["Authorization"]=f"Bearer {self.token}"
        with open(audio_path,"rb") as f:
            files={"file":f}
            async with httpx.AsyncClient(timeout=180) as c:
                r=await c.post(self.base_url+"/transcribe",headers=headers,files=files);r.raise_for_status();return r.json()

class HTTPTTS(TTSProvider):
    def __init__(self, base_url: str, token: str | None = None):
        self.base_url=base_url.rstrip("/"); self.token=token
    async def synthesize(self,text:str,output_path:str)->dict:
        headers={}
        if self.token: headers["Authorization"]=f"Bearer {self.token}"
        async with httpx.AsyncClient(timeout=180) as c:
            r=await c.post(self.base_url+"/synthesize",headers=headers,json={"text":text});r.raise_for_status()
            open(output_path,"wb").write(r.content)
        return {"ok":True,"path":output_path}
