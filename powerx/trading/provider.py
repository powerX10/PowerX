from __future__ import annotations
import os, httpx

class CMSModelProvider:
    def __init__(self, cms_url: str | None = None, token: str | None = None):
        self.cms_url = (cms_url or os.getenv("POWERX_MODEL_CMS_URL", "http://127.0.0.1:8400")).rstrip("/")
        self.token = token or os.getenv("POWERX_CONTROL_TOKEN", "")

    async def candidates(self, capability: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(self.cms_url + "/v1/resolve", headers={"Authorization":f"Bearer {self.token}"}, json={"capability":capability})
            r.raise_for_status()
            return r.json().get("candidates", [])

class OpenAICompatibleRuntime:
    async def chat(self, candidate: dict, messages: list[dict], max_tokens: int = 900) -> dict:
        endpoint = candidate.get("endpoint")
        if not endpoint:
            raise RuntimeError(f"No endpoint configured for {candidate.get('model_id')}")
        async with httpx.AsyncClient(timeout=180) as c:
            r = await c.post(endpoint.rstrip("/") + "/chat/completions", json={"model":candidate["model_id"],"messages":messages,"max_tokens":max_tokens})
            r.raise_for_status()
            return r.json()
