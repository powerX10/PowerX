from powerx.runtime.gpu.profiles.gpt_oss_20b import GPT_OSS_20B
from powerx.runtime.gpu.profiles.qwen_8b import QWEN_8B
from powerx.runtime.gpu.profiles.vision_4b import VISION_4B

GPU_PROFILES = {
    GPT_OSS_20B.id: GPT_OSS_20B,
    QWEN_8B.id: QWEN_8B,
    VISION_4B.id: VISION_4B,
}

def get_gpu_profile(model_id: str):
    try:
        return GPU_PROFILES[model_id]
    except KeyError as exc:
        raise KeyError(f"Unknown GPU profile: {model_id}") from exc
