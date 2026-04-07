from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IP Overseas Risk Multi-Agent Demo"
    openai_api_key: str = Field(default="")
    openai_base_url: str = Field(default="https://api.openai.com/v1")
    openai_model: str = Field(default="gpt-4o-mini")
    embedding_model: str = Field(default="text-embedding-3-small")
    llm_timeout_seconds: int = Field(default=45)
    mock_mode: bool = Field(default=False)
    enable_remote_embedding: bool = Field(default=True)
    default_top_k: int = Field(default=4)

    cors_origins: str = Field(default="*")
    available_agents: List[str] = ["qa", "layout", "litigation"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
