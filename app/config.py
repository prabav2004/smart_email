import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    # FastAPI
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DEBUG: bool = False

    # OpenAI
    OPENAI_API_KEY: str | None = None

    # Hugging Face
    HF_TOKEN: str | None = None

    # LangSmith
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_PROJECT: str = "smart-email-assistant"
    LANGCHAIN_TRACING_V2: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()


# Configure LangSmith
if settings.LANGSMITH_API_KEY:
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY

os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT

os.environ["LANGCHAIN_TRACING_V2"] = (
    "true" if settings.LANGCHAIN_TRACING_V2 else "false"
)