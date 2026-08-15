import httpx
async def openai_chat(runtime, messages, max_tokens):
    headers={"Content-Type":"application/json"}
    if runtime.api_key: headers["Authorization"]=f"Bearer {runtime.api_key}"
    async with httpx.AsyncClient(timeout=240) as c:
        r=await c.post(runtime.base_url.rstrip("/")+"/v1/chat/completions",headers=headers,json={"model":runtime.model_id,"messages":messages,"max_tokens":max_tokens})
        r.raise_for_status(); return r.json()
async def media_generate(runtime, capability, prompt):
    headers={"Content-Type":"application/json"}
    if runtime.api_key: headers["Authorization"]=f"Bearer {runtime.api_key}"
    path="/v1/images/generations" if capability=="image_generate" else "/v1/videos/generations"
    async with httpx.AsyncClient(timeout=900) as c:
        r=await c.post(runtime.base_url.rstrip("/")+path,headers=headers,json={"model":runtime.model_id,"prompt":prompt})
        r.raise_for_status(); return r.json()
