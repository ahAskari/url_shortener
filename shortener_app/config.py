from pydantic import BaseModel
from functools import lru_cache


class Settings(BaseModel):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"

    class Config:
        env_file = '.env'


@lru_cache
def get_settings() -> Settings:
    setting = Settings()
    return setting
