from __future__ import annotations
from typing import Any
from .base import ModelAdapter
from ..errors import AdapterUnavailable, ModelLoadError, InferenceError

class TextClassificationAdapter(ModelAdapter):
    name = "transformers_text_classification"
    def load(self) -> None:
        try:
            from transformers import pipeline
        except Exception as e:
            raise AdapterUnavailable("transformers is required") from e
        try:
            self.pipe = pipeline("text-classification", model=str(self.model_path), tokenizer=str(self.model_path), device_map="auto")
            self.loaded = True
        except Exception as e:
            raise ModelLoadError(str(e)) from e
    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.loaded: self.load()
        req = payload.get("request") or payload
        try:
            out = self.pipe(req.get("text", ""), truncation=True)
            return {"result": out, "adapter": self.name}
        except Exception as e:
            raise InferenceError(str(e)) from e
