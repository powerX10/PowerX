from __future__ import annotations
from .base import ModelAdapter
from ..errors import PowerXError

class GraniteTTMForecastAdapter(ModelAdapter):
    def __init__(self,spec_or_path,model_path=None,device="cpu"):
        self.spec = None if model_path is None else spec_or_path
        self.model_path = str(spec_or_path if model_path is None else model_path)
        self.device=device;self.model=None; self.loaded=False
    def load(self):
        try:
            from tsfm_public.models.tinytimemixer import TinyTimeMixerForPrediction
        except Exception as e:
            raise PowerXError("Granite TTM requires the IBM tsfm package matching the checkpoint") from e
        self.model=TinyTimeMixerForPrediction.from_pretrained(self.model_path,local_files_only=True)
        self.model.to(self.device).eval()
        return self
    def unload(self): self.model=None
    def run(self,payload):
        if self.model is None:self.load()
        import torch
        values=torch.tensor(payload["values"],dtype=torch.float32)
        if values.ndim==1: values=values[:,None]
        values=values[None,:,:]
        with torch.no_grad():
            out=self.model(past_values=values)
        pred=getattr(out,"prediction_outputs",None)
        if pred is None: pred=getattr(out,"predictions",None)
        if pred is None: raise PowerXError("Granite TTM output did not expose predictions")
        horizon=int(payload.get("horizon",12))
        arr=pred.detach().cpu().numpy()[0,:horizon,0].tolist()
        return {"forecast":arr,"model":"granite_ttm"}
