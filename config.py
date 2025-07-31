import os

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    secret_key: str
    database_uri: str
    config: str
    r2_access_key_id: str
    r2_secret_access_key: str
    r2_bucket_name: str
    r2_endpoint_url_s3: str
    r2_public_url: str
    admin_user: str
    admin_pwd: str
    video_categories: list[str] = [
        "New Releases",
        "Comedy & Satire",
        "News & Affairs",
        "Documentaries & Features",
        "Short Films",
        "Docu series",
        "Movies",
        "Entertainment",
        "Comedy",
        "Innovations",
        "Blog companion"
    ]

    model_config = (
        SettingsConfigDict(env_file='.env')
        if os.getenv('CONFIG') == 'development'
        else SettingsConfigDict()
    )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    return settings
