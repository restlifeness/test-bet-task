
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000

    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_NAME: str = 'postgres'

    POOL_PRE_PING_DB: bool = True

    REDIS_BROKER_HOST: str
    REDIS_BROKER_PORT: int
    REDIS_BROKER_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env',
    )


ENV = ProjectSettings()
