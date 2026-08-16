import asyncio
from .identity import IdentityResolver
from .planner import MAPlanner
from .router import targets
from .executor import RuntimeExecutor
from .schema import MARequest,MAResponse
class MAOrchestrator:
    def __init__(self):self.p=MAPlanner();self.e=RuntimeExecutor();self.i=IdentityResolver()
    async def one(self,step,mid,pref):
        errs=[]
        for t in targets(step.capability,pref,step.payload.get('metadata') or {}):
            if not t.endpoint:continue
            try:
                data=await (self.e.direct(t.token,t.endpoint,mid,step.capability,step.payload) if t.runtime_class=="cpu"
                            else self.e.broker(t.token,t.endpoint,t.runtime_class,mid,step.capability,step.payload))
                return {"ok":True,"model_id":mid,"runtime":t.runtime_class,"data":data}
            except Exception as x:errs.append(str(x))
        return {"ok":False,"model_id":mid,"errors":errs}
    async def runstep(self,s,pref):
        ensemble=s.capability in {"financial_sentiment","forecasting","deep_reasoning","chart_analysis"}
        if ensemble:return {"capability":s.capability,"results":[x for x in await asyncio.gather(*[self.one(s,m,pref) for m in s.model_ids]) if x["ok"]]}
        for m in s.model_ids:
            x=await self.one(s,m,pref)
            if x["ok"]:return {"capability":s.capability,"results":[x]}
        return {"capability":s.capability,"results":[]}
    async def run(self,r:MARequest):
        ident=self.i.resolve(r.product_id,r.founder_mode);plan=self.p.plan(r)
        outs=await asyncio.gather(*[self.runstep(s,r.preferred_runtime) for s in plan])
        texts=[];arts=[]
        for o in outs:
            for x in o["results"]:
                d=x["data"];z=d.get("result",d) if isinstance(d,dict) else d
                if isinstance(z,dict):
                    if isinstance(z.get("text"),str):texts.append(z["text"])
                    if any(k in z for k in ("image_b64","video_b64","artifact_url","frames")):arts.append(z)
                    c=z.get("choices")
                    if isinstance(c,list) and c and isinstance(c[0],dict):
                        m=c[0].get("message",{})
                        if isinstance(m,dict) and isinstance(m.get("content"),str):texts.append(m["content"])
        return MAResponse(True,ident.name,"\n\n".join(texts) or None,arts,{"plan":[s.__dict__ for s in plan],"outputs":outs} if ident.expose_model_details else {})
