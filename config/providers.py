from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    enabled: bool
    api_key_env: Optional[str]
    endpoint_env: Optional[str]
    notes: str = ""


PROVIDERS = {
    "modal": ProviderConfig(
        name="Modal",
        enabled=True,
        api_key_env="MODAL_TOKEN_ID",
        endpoint_env="MODAL_ENDPOINT",
        notes="Primary heavy GPU provider for gpt-oss-120b and other large models."
    ),

    "beam": ProviderConfig(
        name="Beam Cloud",
        enabled=True,
        api_key_env="BEAM_API_KEY",
        endpoint_env="BEAM_ENDPOINT",
        notes="Active GPU/CPU provider for finance, strategy, vision and secondary workloads."
    ),

    "cpu": ProviderConfig(
        name="CPU Worker",
        enabled=True,
        api_key_env=None,
        endpoint_env="CPU_WORKER_ENDPOINT",
        notes="Always-on market scanning, indicators, risk, execution and lightweight model workloads."
    ),

    "device": ProviderConfig(
        name="On-Device Runtime",
        enabled=False,
        api_key_env=None,
        endpoint_env=None,
        notes="Future optional Android local-model fallback."
    ),
}


def get_provider(name: str) -> ProviderConfig:
    if name not in PROVIDERS:
        raise KeyError(f"Unknown provider: {name}")
    return PROVIDERS[name]
