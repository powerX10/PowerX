from powerx.core.settings import get_settings
from powerx.providers.openai_compatible import OpenAICompatibleProvider


def build_phase1_providers() -> dict[str, tuple[OpenAICompatibleProvider, str]]:
    s = get_settings()
    providers: dict[str, tuple[OpenAICompatibleProvider, str]] = {}

    if s.gpt_oss_20b_base_url:
        providers["gpt-oss-20b"] = (
            OpenAICompatibleProvider(
                base_url=s.gpt_oss_20b_base_url,
                api_key=s.gpt_oss_20b_api_key,
            ),
            s.gpt_oss_20b_model,
        )

    if s.qwen_8b_base_url:
        providers["qwen-8b"] = (
            OpenAICompatibleProvider(
                base_url=s.qwen_8b_base_url,
                api_key=s.qwen_8b_api_key,
            ),
            s.qwen_8b_model,
        )

    if s.vision_4b_base_url:
        providers["vision-4b"] = (
            OpenAICompatibleProvider(
                base_url=s.vision_4b_base_url,
                api_key=s.vision_4b_api_key,
            ),
            s.vision_4b_model,
        )

    return providers
