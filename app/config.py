import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env using python-dotenv
load_dotenv()


class Settings(BaseSettings):
    # FastAPI Configurations
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DEBUG: bool = True

    # OpenAI API configuration
    OPENAI_API_KEY: str | None = None

    # LangSmith configurations
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_PROJECT: str = "smart-email-assistant"
    LANGSMITH_TRACING: str = "false"

    # Settings config
    model_config = SettingsConfigDict(
        extra="ignore"
    )


# Instantiate settings for global backend imports
settings = Settings()

# Map LangSmith settings to standard LangChain environment variables to enable tracing automatically
if settings.LANGSMITH_API_KEY:
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY
if settings.LANGSMITH_PROJECT:
    os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT
if settings.LANGSMITH_TRACING and settings.LANGSMITH_TRACING.lower() in ("true", "1", "yes"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"


