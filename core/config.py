from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DyStream API"
    app_version: str = "0.1.0"
    debug: bool = True

    tmdb_api_key: str
    tmdb_base_url: str = "https://api.themoviedb.org/3"

    vimeus_api_key: str
    vimeus_base_url: str = "https://vimeus.com"
    vimeus_view_key: str | None = None
    vimeus_timeout: int = 15

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()