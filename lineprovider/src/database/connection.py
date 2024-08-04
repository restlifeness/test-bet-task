
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import DATABASE_SETTINGS


ASYNC_ENGINE = create_async_engine(**DATABASE_SETTINGS)
SessionMaker = sessionmaker(   # type: ignore
    ASYNC_ENGINE,
    class_=AsyncSession,
    expire_on_commit=False
)
