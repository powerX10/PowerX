from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    powerx_env: str = "development"
    powerx_host: str = "0.0.0.0"
    powerx_port: int = 8000

    gpt_oss_20b_base_url: str | None = None
    gpt_oss_20b_api_key: str = "local"
    gpt_oss_20b_model: str = "openai/gpt-oss-20b"

    qwen_8b_base_url: str | None = None
    qwen_8b_api_key: str = "local"
    qwen_8b_model: str = "qwen3-8b"

    vision_4b_base_url: str | None = None
    vision_4b_api_key: str = "local"
    vision_4b_model: str = "gemma-3-4b"


@lru_cache
def get_settings() -> Settings:
    return Settings()
