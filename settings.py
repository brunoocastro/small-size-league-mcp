from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class LLM_Providers(Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"


class MCP_Settings(BaseSettings):
    """
    Settings for the MCP server.
    This class uses Pydantic to manage configuration settings.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    LLM_PROVIDER: LLM_Providers = LLM_Providers.OPENAI
    LLM_API_KEY: str = ""
    LLM_HOST: str = "https://api.openai.com/v1/chat/completions"
    LLM_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
