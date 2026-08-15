from dataclasses import dataclass
@dataclass(frozen=True)
class EscalationDecision:
    heavy: bool
    requested_tier: str
    reason: str

HEAVY={"image_generate","video_generate","large_vision","deep_reasoning"}

def classify(capability,prompt_chars=0,requested_tier=None):
    if requested_tier:
        return EscalationDecision(requested_tier=="gpu-heavy",requested_tier,"explicit")
    if capability in HEAVY:
        return EscalationDecision(True,"gpu-heavy","heavy capability")
    if prompt_chars>30000:
        return EscalationDecision(True,"6b","large context")
    if capability in {"code","research","reasoning"}:
        return EscalationDecision(False,"4b","balanced")
    return EscalationDecision(False,"3b","continuous/light")
