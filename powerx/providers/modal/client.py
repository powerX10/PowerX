import os
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ModalResponse:
    ok: bool
    data: Dict[str, Any]
    error: str | None = None


class ModalClient:
    def __init__(self):
        self.endpoint = os.getenv("MODAL_ENDPOINT")
        self.token_id = os.getenv("MODAL_TOKEN_ID")
        self.token_secret = os.getenv("MODAL_TOKEN_SECRET")

    def configured(self) -> bool:
        return bool(self.endpoint and self.token_id and self.token_secret)

    def health(self) -> ModalResponse:
        return ModalResponse(
            ok=self.configured(),
            data={
                "provider": "modal",
                "configured": self.configured(),
                "endpoint": bool(self.endpoint),
            },
            error=None if self.configured() else "Modal environment variables are not configured yet.",
        )
