from __future__ import annotations
from .base import ModelAdapter
from ..errors import PowerXError

class MoiraiForecastAdapter(ModelAdapter):
    def __init__(self,spec_or_path,model_path=None,device="cpu"):
        self.spec = None if model_path is None else spec_or_path
        self.model_path = str(spec_or_path if model_path is None else model_path)
        self.device=device;self.model=None; self.loaded=False
    def load(self):
        try:
            from uni2ts.model.moirai import MoiraiForecast, MoiraiModule
        except Exception as e:
            raise PowerXError("Moirai requires uni2ts with Moirai support") from e
        self.module=MoiraiModule.from_pretrained(self.model_path,local_files_only=True)
        return self
    def unload(self): self.model=None
    def run(self,payload):
        raise PowerXError(
            "Moirai checkpoint is installed, but dataset-shaped inference must be wired to the exact uni2ts release. "
            "Use Chronos/TimesFM in production until scripts/verify_moirai_api.py passes."
        )
