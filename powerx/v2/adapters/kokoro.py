from __future__ import annotations
import base64, io, os
from typing import Any
from .base import ModelAdapter
from ..errors import AdapterUnavailable, ModelLoadError, InferenceError

class KokoroAdapter(ModelAdapter):
    name = "kokoro"
    def load(self) -> None:
        try:
            from kokoro import KPipeline
        except Exception as e:
            raise AdapterUnavailable("kokoro package is required for Kokoro TTS") from e
        try:
            self.pipeline = KPipeline(lang_code=os.getenv("POWERX_KOKORO_LANG", "a"), repo_id=str(self.model_path))
            self.loaded = True
        except TypeError:
            try:
                self.pipeline = KPipeline(lang_code=os.getenv("POWERX_KOKORO_LANG", "a"))
                self.loaded = True
            except Exception as e:
                raise ModelLoadError(str(e)) from e
        except Exception as e:
            raise ModelLoadError(str(e)) from e

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.loaded: self.load()
        req = payload.get("request") or payload
        text = req.get("text", "")
        voice = (req.get("metadata") or {}).get("voice", os.getenv("POWERX_KOKORO_VOICE", "af_heart"))
        try:
            import soundfile as sf
            chunks = []
            for _, _, audio in self.pipeline(text, voice=voice, speed=float((req.get("metadata") or {}).get("speed", 1.0))):
                chunks.append(audio)
            if not chunks:
                raise InferenceError("Kokoro returned no audio")
            import numpy as np
            audio = np.concatenate(chunks)
            buf = io.BytesIO(); sf.write(buf, audio, 24000, format="WAV")
            return {"audio_b64": base64.b64encode(buf.getvalue()).decode(), "mime_type":"audio/wav", "sample_rate":24000, "adapter":self.name}
        except Exception as e:
            if isinstance(e, InferenceError): raise
            raise InferenceError(str(e)) from e
