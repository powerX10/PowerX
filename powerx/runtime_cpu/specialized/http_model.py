from typing import Any
import httpx
from powerx.runtime_cpu.specialized.base import SpecializedModel


class HTTPSpecializedModel(SpecializedModel):
    def __init__(
        self,
        *,
        base_url: str,
        infer_path: str = "/infer",
        health_path: str = "/health",
        bearer_token: str | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.infer_path = infer_path
        self.health_path = health_path
        self.bearer_token = bearer_token

    def _headers(self):
        if not self.bearer_token:
            return {}
        return {"Authorization": f"Bearer {self.bearer_token}"}

    async def infer(self, payload: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(
                self.base_url + self.infer_path,
                json=payload,
                headers=self._headers(),
            )
            r.raise_for_status()
            return r.json()

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(
                    self.base_url + self.health_path,
                    headers=self._headers(),
                )
                return r.is_success
        except httpx.HTTPError:
            return False
