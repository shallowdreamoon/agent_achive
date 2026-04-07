from functools import lru_cache
from typing import List
import os

from pydantic import BaseModel, Field


class Settings(BaseModel):
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


def _parse_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "IP Overseas Risk Multi-Agent Demo"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        llm_timeout_seconds=int(os.getenv("LLM_TIMEOUT_SECONDS", "45")),
        mock_mode=_parse_bool(os.getenv("MOCK_MODE"), False),
        enable_remote_embedding=_parse_bool(os.getenv("ENABLE_REMOTE_EMBEDDING"), True),
        default_top_k=int(os.getenv("DEFAULT_TOP_K", "4")),
        cors_origins=os.getenv("CORS_ORIGINS", "*"),
        available_agents=["qa", "layout", "litigation"],
    )
