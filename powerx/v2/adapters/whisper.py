from __future__ import annotations
import base64, tempfile
from pathlib import Path
from typing import Any
from .base import ModelAdapter
from ..errors import AdapterUnavailable, ModelLoadError, InferenceError

class WhisperAdapter(ModelAdapter):
    name = "whisper"
    def load(self) -> None:
        try:
            import torch
            from transformers import pipeline
        except Exception as e:
            raise AdapterUnavailable("torch + transformers are required for Whisper") from e
        try:
            device = 0 if torch.cuda.is_available() else -1
            self.pipe = pipeline("automatic-speech-recognition", model=str(self.model_path), tokenizer=str(self.model_path), feature_extractor=str(self.model_path), device=device)
            self.loaded = True
        except Exception as e:
            raise ModelLoadError(str(e)) from e

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.loaded: self.load()
        req = payload.get("request") or payload
        md = req.get("metadata") or {}
        path = md.get("audio_path")
        raw = md.get("audio_b64")
        temp = None
        if not path and raw:
            temp = tempfile.NamedTemporaryFile(suffix=md.get("audio_suffix", ".wav"), delete=False)
            temp.write(base64.b64decode(raw)); temp.close(); path = temp.name
        if not path:
            raise InferenceError("Whisper requires metadata.audio_path or metadata.audio_b64")
        try:
            out = self.pipe(path)
            return {"text": out.get("text", ""), "adapter": self.name}
        finally:
            if temp:
                Path(temp.name).unlink(missing_ok=True)
