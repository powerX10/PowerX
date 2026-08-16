from __future__ import annotations
from .schema import AgentFinding

STANCE_SCORE = {"strong_bearish":-2.0,"bearish":-1.0,"neutral":0.0,"bullish":1.0,"strong_bullish":2.0}

def weighted_consensus(findings: list[AgentFinding], weights: dict[str, float]) -> tuple[str, float, list[str]]:
    if not findings:
        return "neutral", 0.0, ["No agent findings available"]
    total_w = 0.0
    score = 0.0
    conflicts = []
    signs = set()
    for f in findings:
        w = max(0.0, weights.get(f.role, 1.0)) * max(0.05, f.confidence)
        s = STANCE_SCORE.get(f.stance, 0.0)
        score += w * s
        total_w += 2.0 * w
        if s > 0: signs.add("bullish")
        if s < 0: signs.add("bearish")
    normalized = 0.0 if total_w == 0 else score / total_w
    if len(signs) > 1:
        conflicts.append("Bullish and bearish specialist signals disagree")
    if normalized >= .55: stance = "strong_bullish"
    elif normalized >= .15: stance = "bullish"
    elif normalized <= -.55: stance = "strong_bearish"
    elif normalized <= -.15: stance = "bearish"
    else: stance = "neutral"
    confidence = min(1.0, abs(normalized) + (0.20 if len(findings) >= 5 else 0.0))
    return stance, round(confidence, 3), conflicts
