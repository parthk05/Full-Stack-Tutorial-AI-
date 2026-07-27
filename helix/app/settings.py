"""
Step 1.1 / 1.2 — App settings loaded from .env

Why: keeps secrets out of source code and lets model name change without redeploying code.
"""
#lru_cache is used to cache the settings
from functools import lru_cache
#SettingConfigDict is used to load the settings from the .env file
#BaseSettings is the base class for the settings
#SettingsConfigDict is the configuration for the settings
from pydantic_settings import BaseSettings, SettingsConfigDict

#Settings is the class for the settings
#It inherits from BaseSettings and SettingsConfigDict
class Settings(BaseSettings):
    # Step 1.1 — names match helix/.env (LLM_API_Key, MODEL_NAME)
    LLM_API_Key: str
    MODEL_NAME: str = "gemini-2.5-flash"

    # Step 4.2 preview — bump when you change system prompts so evals can compare versions
    PROMPT_VERSION: str = "prompt_desk_v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    # Step 1.2 — cache so every request does not re-read .env from disk
    return Settings()
