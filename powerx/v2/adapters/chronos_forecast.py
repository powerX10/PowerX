from __future__ import annotations
from .base import ModelAdapter
from ..errors import PowerXError

class ChronosForecastAdapter(ModelAdapter):
    def __init__(self, spec_or_path, model_path=None, device="cpu"):
        self.spec = None if model_path is None else spec_or_path
        self.model_path = str(spec_or_path if model_path is None else model_path)
        self.device=device; self.pipe=None; self.loaded=False
    def load(self):
        try:
            from chronos import ChronosPipeline
            import torch
        except Exception as e:
            raise PowerXError("Chronos adapter requires chronos-forecasting and torch") from e
        self.pipe=ChronosPipeline.from_pretrained(self.model_path, device_map=self.device, local_files_only=True)
        return self
    def unload(self): self.pipe=None
    def run(self,payload):
        if self.pipe is None:self.load()
        import torch
        values=payload["values"]; horizon=int(payload.get("horizon",12)); samples=int(payload.get("samples",20))
        pred=self.pipe.predict(torch.tensor(values,dtype=torch.float32),prediction_length=horizon,num_samples=samples)
        x=pred.detach().cpu()
        median=x.median(dim=0).values.tolist()
        return {"forecast":median,"samples_shape":list(x.shape),"model":"chronos"}
