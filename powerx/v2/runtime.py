from __future__ import annotations
import httpx
from .settings import PowerXSettings
from .registry import ModelRegistry
from .schema import PowerXRequest, PowerXResponse, ModelSpec

CAPABILITY_KEYWORDS = [
    (("video", "mp4", "course video"), "video_generate"),
    (("image", "photo", "thumbnail"), "image_generate"),
    (("transcribe", "speech to text", "stt"), "speech_to_text"),
    (("voice", "speak", "tts", "read aloud"), "text_to_speech"),
    (("chart", "nifty", "trade", "trading", "breakout", "support", "resistance"), "trading_analysis"),
    (("code", "repo", "github", "fix", "bug"), "coding"),
]

def infer_capability(text: str) -> str:
    t=text.lower()
    for keys,cap in CAPABILITY_KEYWORDS:
        if any(k in t for k in keys): return cap
    return "chat"

class RuntimeBroker:
    def __init__(self):
        self.settings=PowerXSettings.load(); self.registry=ModelRegistry()
    def select_model(self, req:PowerXRequest)->ModelSpec:
        cap=req.capability or infer_capability(req.text)
        models=self.registry.best_for(cap, req.preferred_runtime) or self.registry.best_for("chat", req.preferred_runtime)
        if not models: raise RuntimeError(f"No model for capability={cap}")
        requested=(req.metadata or {}).get("model_id")
        if requested:
            return self.registry.by_id(requested)
        return models[0]
    async def run(self, req:PowerXRequest)->PowerXResponse:
        spec=self.select_model(req); cap=req.capability or infer_capability(req.text)
        if self.settings.mock_mode:
            return PowerXResponse(ok=True,model_id=spec.id,runtime="mock",text=f"PowerX V2 mock ok: {spec.id}",data={"capability":cap})
        if not self.settings.lightning_worker_url:
            return PowerXResponse(ok=False,model_id=spec.id,runtime="lightning",errors=["POWERX_LIGHTNING_WORKER_URL missing"])
        headers={}
        if self.settings.lightning_worker_token: headers["Authorization"]=f"Bearer {self.settings.lightning_worker_token}"
        # Important: remote worker owns Drive->local cache. Do not send a host-local model_path.
        payload={"model":spec.model_dump(),"request":req.model_dump(),"capability":cap}
        try:
            async with httpx.AsyncClient(timeout=float((req.metadata or {}).get("worker_timeout_sec",3600))) as client:
                r=await client.post(self.settings.lightning_worker_url.rstrip("/")+"/v1/run",json=payload,headers=headers)
                r.raise_for_status(); data=r.json()
            return PowerXResponse(ok=bool(data.get("ok",True)),model_id=spec.id,runtime="lightning",text=data.get("text"),artifact_url=data.get("artifact_url"),data=data,errors=data.get("errors",[]))
        except Exception as e:
            return PowerXResponse(ok=False,model_id=spec.id,runtime="lightning",errors=[str(e)])
