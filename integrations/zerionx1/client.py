from __future__ import annotations
from typing import Any
import httpx


class PowerXClient:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float = 180.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    async def chat(
        self,
        *,
        task: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 1024,
        request_id: str | None = None,
    ) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if request_id:
            headers["X-Request-ID"] = request_id

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.base_url + "/v1/inference/chat",
                headers=headers,
                json={
                    "task": task,
                    "messages": messages,
                    "max_tokens": max_tokens,
                },
            )
            response.raise_for_status()
            return response.json()

    async def ready(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(self.base_url + "/ready")
            response.raise_for_status()
            return response.json()
