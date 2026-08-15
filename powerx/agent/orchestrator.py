import json, httpx
from .capabilities import infer_capability
from .providers import openai_chat, media_generate
from .schema import AgentResponse
from .tool_registry import default_tools

SYSTEM="""You are PowerX Agent, a private multimodel orchestration assistant. You can reason, code, analyze files/images, research through configured tools, and route image/video/voice jobs. Request a tool only with one JSON line: {"tool":"TOOL_NAME","arguments":{...}}. Never claim an action succeeded unless its tool returned success."""

class UniversalAgent:
    def __init__(self,scheduler): self.scheduler=scheduler; self.tools=default_tools()
    async def _healthy(self,r):
        try:
            async with httpx.AsyncClient(timeout=3) as c: return (await c.get(r.base_url.rstrip("/")+"/health")).status_code < 500
        except Exception: return False
    async def _pick(self,cap):
        for r in self.scheduler.candidates(cap):
            if await self._healthy(r): return r
        raise RuntimeError(f"No healthy runtime for capability '{cap}'")
    async def run(self,req):
        cap=req.capability or infer_capability(req.messages,req.attachments)
        try: runtime=await self._pick(cap)
        except Exception as e: return AgentResponse(ok=False,capability=cap,error=str(e))
        if cap in {"image_generate","video_generate"}:
            try:
                out=await media_generate(runtime,cap,str(req.messages[-1].get("content","")))
                return AgentResponse(ok=True,capability=cap,model_id=runtime.model_id,runtime_id=runtime.id,output=out)
            except Exception as e:
                return AgentResponse(ok=False,capability=cap,model_id=runtime.model_id,runtime_id=runtime.id,error=str(e))
        messages=[{"role":"system","content":SYSTEM+"\nAvailable tools:\n"+json.dumps(self.tools.specs())},*req.messages]
        events=[]
        for _ in range(6):
            try: out=await openai_chat(runtime,messages,req.max_tokens)
            except Exception as e: return AgentResponse(ok=False,capability=cap,model_id=runtime.model_id,runtime_id=runtime.id,tool_events=events,error=str(e))
            content=(((out.get("choices") or [{}])[0].get("message") or {}).get("content") or "")
            tr=None
            for line in content.splitlines():
                if line.strip().startswith('{"tool"'):
                    try: tr=json.loads(line.strip())
                    except Exception: pass
                    break
            if not req.allow_tools or not tr:
                return AgentResponse(ok=True,capability=cap,model_id=runtime.model_id,runtime_id=runtime.id,output=out,tool_events=events)
            try:
                t=self.tools.get(tr["tool"]); result=await t.fn(tr.get("arguments") or {}); events.append({"tool":t.name,"ok":True,"result":result})
            except Exception as e:
                result={"ok":False,"error":str(e)}; events.append({"tool":tr.get("tool"),"ok":False,"error":str(e)})
            messages += [{"role":"assistant","content":content},{"role":"user","content":"TOOL_RESULT:\n"+json.dumps(result)}]
        return AgentResponse(ok=False,capability=cap,model_id=runtime.model_id,runtime_id=runtime.id,tool_events=events,error="Tool loop limit reached")
