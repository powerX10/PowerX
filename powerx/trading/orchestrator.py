from __future__ import annotations
import asyncio, json
from .roles import TradingRoleRegistry
from .schema import TradingRequest, TradingReport, AgentFinding
from .consensus import weighted_consensus
from .prompts import BEGINNER_GUARDRAIL

class TradingSwarmOrchestrator:
    def __init__(self, roles, model_provider, runtime_client):
        self.roles = roles
        self.model_provider = model_provider
        self.runtime_client = runtime_client

    def _context(self, req: TradingRequest) -> dict:
        return {
            "symbol": req.symbol, "market": req.market, "timeframe": req.timeframe,
            "query": req.query, "user_level": req.user_level,
            "price_data": req.price_data[-500:], "indicators": req.indicators,
            "fundamentals": req.fundamentals, "news": req.news[-50:],
            "derivatives": req.derivatives, "portfolio": req.portfolio,
            "chart_image_url": req.chart_image_url,
        }

    async def _run_role(self, role, req: TradingRequest) -> AgentFinding:
        candidates = await self.model_provider.candidates(role.capability)
        if not candidates:
            return AgentFinding(role=role.id, summary="No configured model/runtime for this specialist", risks=["specialist unavailable"])
        context = self._context(req)
        messages = [
            {"role":"system","content": role.prompt + "\n" + BEGINNER_GUARDRAIL + "\nReturn strict JSON: stance, confidence, summary, evidence[], risks[]."},
            {"role":"user","content":json.dumps(context, default=str)},
        ]
        last = None
        for candidate in candidates[:3]:
            try:
                raw = await self.runtime_client.chat(candidate, messages)
                text = (((raw.get("choices") or [{}])[0].get("message") or {}).get("content") or "{}")
                data = json.loads(text[text.find("{"):text.rfind("}")+1])
                return AgentFinding(role=role.id, model_id=candidate.get("model_id"), stance=data.get("stance","neutral"), confidence=float(data.get("confidence",0.0)), summary=data.get("summary",text[:1200]), evidence=data.get("evidence",[]), risks=data.get("risks",[]), raw={"runtime_class":candidate.get("runtime_class")})
            except Exception as exc:
                last = exc
        return AgentFinding(role=role.id, summary=f"Specialist failed: {last}", risks=["runtime failure"])

    async def run(self, req: TradingRequest) -> TradingReport:
        roles = self.roles.all()
        findings = await asyncio.gather(*(self._run_role(r, req) for r in roles))
        weights = {r.id:r.weight for r in roles}
        consensus, confidence, conflicts = weighted_consensus(findings, weights)
        evidence = [f.summary for f in findings if f.confidence >= .35][:6]
        beginner = f"PowerX specialists currently lean {consensus.replace('_',' ')} with {round(confidence*100)}% consensus confidence. " + (" Key points: " + " | ".join(evidence) if evidence else "Specialists do not yet have enough reliable evidence.")
        return TradingReport(symbol=req.symbol, market=req.market, timeframe=req.timeframe, consensus=consensus, confidence=confidence, beginner_explanation=beginner, findings=findings, conflicts=conflicts, risk_controls={"require_user_confirmation":True,"guaranteed_profit":False,"max_position_size":"configured by Zerion risk engine"})
