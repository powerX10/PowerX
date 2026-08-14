from powerx.runtime_cpu.llamacpp.profile import LlamaCppProfile

CPU_PROFILES = {
    "qwen-4b-local": LlamaCppProfile(
        id="qwen-4b-local",
        model_path_env="POWERX_QWEN4B_GGUF",
        served_model_name="qwen-4b-local",
        context_size=16384,
        threads=6,
        batch_size=256,
    ),
    "phi-mini-local": LlamaCppProfile(
        id="phi-mini-local",
        model_path_env="POWERX_PHI_MINI_GGUF",
        served_model_name="phi-mini-local",
        context_size=16384,
        threads=6,
        batch_size=256,
    ),
    "gemma-1b-local": LlamaCppProfile(
        id="gemma-1b-local",
        model_path_env="POWERX_GEMMA1B_GGUF",
        served_model_name="gemma-1b-local",
        context_size=8192,
        threads=4,
        batch_size=192,
    ),
}

def get_cpu_profile(model_id: str) -> LlamaCppProfile:
    try:
        return CPU_PROFILES[model_id]
    except KeyError as exc:
        raise KeyError(f"Unknown CPU model profile: {model_id}") from exc
