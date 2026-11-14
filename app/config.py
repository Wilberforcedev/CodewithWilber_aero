from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Code with Wilber"
    environment: str = "development"
    database_url: str = "sqlite:///./wilber.db"
    site_url: str = "http://localhost:8000"
    contact_email: str = "hello@codewithwilber.com"
    checkout_url: str = ""
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

