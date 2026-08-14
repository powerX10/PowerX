import json
import httpx

async def stream_chat(base_url:str, api_key:str|None, payload:dict):
    headers={"Content-Type":"application/json"}
    if api_key: headers["Authorization"]=f"Bearer {api_key}"
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST",base_url.rstrip("/")+"/chat/completions",headers=headers,json={**payload,"stream":True}) as r:
            r.raise_for_status()
            async for line in r.aiter_lines():
                if not line.startswith("data:"): continue
                data=line[5:].strip()
                if data=="[DONE]": break
                try:
                    obj=json.loads(data)
                    delta=obj.get("choices",[{}])[0].get("delta",{}).get("content")
                    if delta: yield delta
                except Exception:
                    continue
