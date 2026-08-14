import os
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class BeamResponse:
    ok: bool
    data: Dict[str, Any]
    error: str | None = None


class BeamClient:
    def __init__(self):
        self.endpoint = os.getenv("BEAM_ENDPOINT")
        self.api_key = os.getenv("BEAM_API_KEY")

    def configured(self) -> bool:
        return bool(self.endpoint and self.api_key)

    def health(self) -> BeamResponse:
        return BeamResponse(
            ok=self.configured(),
            data={
                "provider": "beam",
                "configured": self.configured(),
                "endpoint": bool(self.endpoint),
            },
            error=None if self.configured() else "Beam environment variables are not configured yet.",
        )
