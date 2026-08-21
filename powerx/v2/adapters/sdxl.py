from __future__ import annotations
from pathlib import Path
from .base import ModelAdapter
from ..errors import PowerXError

class SDXLAdapter(ModelAdapter):
    def __init__(self, spec_or_path, model_path=None, device="cuda", dtype="float16"):
        self.spec = None if model_path is None else spec_or_path
        self.model_path = str(spec_or_path if model_path is None else model_path)
        self.device=device; self.dtype=dtype; self.pipe=None; self.loaded=False

    def load(self):
        try:
            import torch
            from diffusers import StableDiffusionXLPipeline
        except Exception as e:
            raise PowerXError("SDXL requires torch + diffusers + transformers + accelerate") from e
        dt=torch.float16 if self.dtype=="float16" else torch.bfloat16
        self.pipe=StableDiffusionXLPipeline.from_pretrained(
            self.model_path, torch_dtype=dt, local_files_only=True, use_safetensors=True
        ).to(self.device)
        return self

    def unload(self):
        self.pipe=None
        try:
            import torch
            if torch.cuda.is_available(): torch.cuda.empty_cache()
        except Exception: pass

    def run(self, payload: dict):
        if self.pipe is None: self.load()
        prompt=payload.get("prompt") or payload.get("text")
        if not prompt: raise ValueError("prompt required")
        negative=payload.get("negative_prompt")
        width=int(payload.get("width",1024)); height=int(payload.get("height",1024))
        steps=int(payload.get("steps",30)); guidance=float(payload.get("guidance_scale",5.5))
        img=self.pipe(prompt=prompt, negative_prompt=negative, width=width, height=height,
                      num_inference_steps=steps, guidance_scale=guidance).images[0]
        out=Path(payload.get("output_path","output.png")); out.parent.mkdir(parents=True,exist_ok=True)
        img.save(out)
        return {"artifact_url":str(out),"kind":"image","width":width,"height":height}
