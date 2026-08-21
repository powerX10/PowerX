from __future__ import annotations
import os
from typing import Any
from .base import ModelAdapter
from ..errors import AdapterUnavailable, ModelLoadError, InferenceError

class TransformersTextAdapter(ModelAdapter):
    name = "transformers_text_generation"
    def load(self) -> None:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except Exception as e:
            raise AdapterUnavailable("torch + transformers are required") from e
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(str(self.model_path), local_files_only=True, trust_remote_code=True)
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            self.model = AutoModelForCausalLM.from_pretrained(str(self.model_path), local_files_only=True, trust_remote_code=True, torch_dtype=dtype, device_map="auto" if torch.cuda.is_available() else None)
            self.device = next(self.model.parameters()).device
            self.loaded = True
        except Exception as e:
            raise ModelLoadError(str(e)) from e

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.loaded: self.load()
        req = payload.get("request") or payload
        text = req.get("text", "")
        messages = req.get("messages") or [{"role":"user","content":text}]
        try:
            if hasattr(self.tokenizer, "apply_chat_template"):
                prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            else:
                prompt = "\n".join(f"{m.get('role','user')}: {m.get('content','')}" for m in messages)
            toks = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            out = self.model.generate(**toks, max_new_tokens=int(req.get("metadata",{}).get("max_tokens",1024)), do_sample=False)
            new = out[0][toks["input_ids"].shape[-1]:]
            return {"text": self.tokenizer.decode(new, skip_special_tokens=True), "adapter": self.name}
        except Exception as e:
            raise InferenceError(str(e)) from e
