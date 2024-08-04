
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_NAME: str = 'postgres'

    POOL_PRE_PING_DB: bool = True

    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 5739


ENV = ProjectSettings()
