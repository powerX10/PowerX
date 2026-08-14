from dataclasses import dataclass


@dataclass(frozen=True)
class MobileModelSlot:
    id: str
    env_var: str
    max_recommended_file_gb: float
    role: str


MOBILE_MODEL_SLOTS = {
    "mobile-primary": MobileModelSlot(
        id="mobile-primary",
        env_var="POWERX_MOBILE_PRIMARY_GGUF",
        max_recommended_file_gb=3.5,
        role="general local fallback",
    ),
    "mobile-small": MobileModelSlot(
        id="mobile-small",
        env_var="POWERX_MOBILE_SMALL_GGUF",
        max_recommended_file_gb=2.0,
        role="fast local assistant and routing",
    ),
    "mobile-guard": MobileModelSlot(
        id="mobile-guard",
        env_var="POWERX_MOBILE_GUARD_GGUF",
        max_recommended_file_gb=1.5,
        role="local safety/guard checks",
    ),
}
