from __future__ import annotations
from .base import ModelAdapter
from ..errors import PowerXError

class TimesFMForecastAdapter(ModelAdapter):
    def __init__(self, spec_or_path, model_path=None, device="cpu"):
        self.spec = None if model_path is None else spec_or_path
        self.model_path = str(spec_or_path if model_path is None else model_path)
        self.device=device; self.model=None; self.loaded=False
    def load(self):
        try:
            import timesfm
        except Exception as e:
            raise PowerXError("TimesFM adapter requires the timesfm package compatible with your checkpoint") from e
        if hasattr(timesfm,"TimesFm"):
            try:
                self.model=timesfm.TimesFm(checkpoint_path=self.model_path)
            except TypeError:
                raise PowerXError("Your installed TimesFM API differs; configure this adapter for that checkpoint release")
        else:
            raise PowerXError("Installed timesfm package has no TimesFm class")
        return self
    def unload(self): self.model=None
    def run(self,payload):
        if self.model is None:self.load()
        import numpy as np
        values=np.asarray(payload["values"],dtype=np.float32)
        horizon=int(payload.get("horizon",12))
        result=self.model.forecast([values],freq=[int(payload.get("freq",0))])
        point=result[0] if isinstance(result,tuple) else result
        arr=np.asarray(point)[0][:horizon].tolist()
        return {"forecast":arr,"model":"timesfm"}
