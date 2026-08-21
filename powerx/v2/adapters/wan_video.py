from __future__ import annotations
from pathlib import Path
from .base import ModelAdapter
from ..errors import PowerXError

class WanVideoAdapter(ModelAdapter):
    """Diffusers Wan adapter. Tested interface is selected dynamically to tolerate supported diffusers versions."""
    def __init__(self, spec_or_path, model_path=None, device="cuda", dtype="bfloat16"):
        self.spec = None if model_path is None else spec_or_path
        self.model_path = str(spec_or_path if model_path is None else model_path)
        self.device=device; self.dtype=dtype; self.pipe=None; self.loaded=False

    def load(self):
        try:
            import torch, diffusers
        except Exception as e:
            raise PowerXError("Wan requires torch + a diffusers version containing WanPipeline") from e
        WanPipeline=getattr(diffusers,"WanPipeline",None)
        if WanPipeline is None:
            raise PowerXError("Installed diffusers has no WanPipeline; upgrade to a Wan-supported diffusers build")
        dt=torch.bfloat16 if self.dtype=="bfloat16" else torch.float16
        self.pipe=WanPipeline.from_pretrained(self.model_path, torch_dtype=dt, local_files_only=True)
        if hasattr(self.pipe,"enable_model_cpu_offload"):
            self.pipe.enable_model_cpu_offload()
        else:
            self.pipe.to(self.device)
        return self

    def unload(self):
        self.pipe=None
        try:
            import torch
            if torch.cuda.is_available(): torch.cuda.empty_cache()
        except Exception: pass

    def run(self, payload: dict):
        if self.pipe is None: self.load()
        try:
            from diffusers.utils import export_to_video
        except Exception as e:
            raise PowerXError("diffusers export_to_video unavailable") from e
        prompt=payload.get("prompt") or payload.get("text")
        if not prompt: raise ValueError("prompt required")
        width=int(payload.get("width",1280)); height=int(payload.get("height",720))
        fps=int(payload.get("fps",24))
        frames=int(payload.get("num_frames",81))
        steps=int(payload.get("steps",30))
        kwargs={"prompt":prompt,"height":height,"width":width,"num_frames":frames,"num_inference_steps":steps}
        if payload.get("negative_prompt"): kwargs["negative_prompt"]=payload["negative_prompt"]
        result=self.pipe(**kwargs)
        video_frames=getattr(result,"frames",None)
        if isinstance(video_frames,list) and video_frames and isinstance(video_frames[0],list):
            video_frames=video_frames[0]
        if not video_frames:
            raise PowerXError("WanPipeline returned no frames")
        out=Path(payload.get("output_path","segment.mp4")); out.parent.mkdir(parents=True,exist_ok=True)
        export_to_video(video_frames,str(out),fps=fps)
        return {"artifact_url":str(out),"kind":"video","frames":len(video_frames),"fps":fps}
