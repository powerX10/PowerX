from __future__ import annotations
import httpx

class PowerXTradingClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 240.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    async def analyze(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(self.base_url + "/v1/trading/analyze", headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"}, json=payload)
            r.raise_for_status()
            return r.json()
