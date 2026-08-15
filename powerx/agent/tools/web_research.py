import os, httpx
from .base import Tool
async def web_search(args):
    url=os.getenv("POWERX_WEB_SEARCH_URL")
    if not url: return {"ok":False,"error":"POWERX_WEB_SEARCH_URL not configured"}
    headers={"Content-Type":"application/json"}
    if os.getenv("POWERX_WEB_SEARCH_KEY"): headers["Authorization"]=f"Bearer {os.getenv('POWERX_WEB_SEARCH_KEY')}"
    async with httpx.AsyncClient(timeout=90) as c:
        r=await c.post(url,headers=headers,json={"query":args["query"],"top_k":args.get("top_k",8)})
        r.raise_for_status(); return r.json()
TOOLS=[Tool("web_search","Search current web through configured adapter.",web_search)]
