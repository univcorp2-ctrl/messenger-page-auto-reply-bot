from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    verify_token: str = "change-me"
    page_access_token: str | None = None
    page_id: str | None = None
    graph_api_version: str = "v25.0"
    app_secret: str | None = None
    auto_reply_enabled: bool = True
    send_real_messages: bool = False
    database_url: str = "sqlite:///./messenger_events.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
