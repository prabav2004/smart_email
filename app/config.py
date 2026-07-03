import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded automatically from .env
    """

    # =====================================================
    # FastAPI Configuration
    # =====================================================
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DEBUG: bool = True

    # =====================================================
    # OpenAI Configuration
    # =====================================================
    OPENAI_API_KEY: str | None = None

    # =====================================================
    # LangSmith Configuration
    # =====================================================
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_PROJECT: str = "smart-email-assistant"
    LANGCHAIN_TRACING_V2: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Global settings object
settings = Settings()


# ---------------------------------------------------------
# Configure LangSmith Environment Variables
# ---------------------------------------------------------

if settings.LANGSMITH_API_KEY:
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY

os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT

if settings.LANGCHAIN_TRACING_V2:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"