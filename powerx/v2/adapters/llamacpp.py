from __future__ import annotations
import os
from typing import Any
from .base import ModelAdapter
from .utils import first_file
from ..errors import AdapterUnavailable, ModelLoadError, InferenceError

class LlamaCppAdapter(ModelAdapter):
    name = "llamacpp"
    def load(self) -> None:
        try:
            from llama_cpp import Llama
        except Exception as e:
            raise AdapterUnavailable("llama-cpp-python is required for GGUF models") from e
        gguf = first_file(self.model_path, (".gguf",))
        n_ctx = int(os.getenv("POWERX_LLAMACPP_CTX", "8192"))
        n_gpu_layers = int(os.getenv("POWERX_LLAMACPP_GPU_LAYERS", "-1"))
        try:
            self.model = Llama(model_path=str(gguf), n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, verbose=False)
            self.loaded = True
        except Exception as e:
            raise ModelLoadError(f"Failed to load GGUF {gguf.name}: {e}") from e

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.loaded: self.load()
        req = payload.get("request") or payload
        messages = req.get("messages") or []
        text = req.get("text", "")
        if not messages:
            messages = [{"role":"system","content":"You are MA, the PowerX assistant. Be accurate and concise."},{"role":"user","content":text}]
        try:
            out = self.model.create_chat_completion(messages=messages, temperature=float(req.get("metadata",{}).get("temperature",0.2)), max_tokens=int(req.get("metadata",{}).get("max_tokens",1024)))
            content = out["choices"][0]["message"]["content"]
            return {"text": content, "usage": out.get("usage", {}), "adapter": self.name}
        except Exception as e:
            raise InferenceError(str(e)) from e
