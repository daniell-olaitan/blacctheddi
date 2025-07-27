import os

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    secret_key: str
    database_uri: str
    config: str

    model_config = (
        SettingsConfigDict(env_file='.env')
        if os.getenv('CONFIG') == 'development'
        else SettingsConfigDict()
    )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    return settings
