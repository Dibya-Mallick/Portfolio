"""Application settings loaded from environment variables."""

import asyncio
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Settings(BaseSettings):
    """Portfolio API configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    APP_ENV: str = "development"
    DATABASE_URL: str = (
        "postgresql+psycopg://portfolio_user:change_me@localhost:5432/portfolio"
    )
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    SECRET_KEY: str = "replace_with_a_secure_random_value"
    EMAIL_PROVIDER_API_KEY: str = ""
    CONTACT_NOTIFICATION_EMAIL: str = ""


settings = Settings()
