import pytest

from typing import AsyncGenerator

from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from main import app

from src.database.models import BaseModel
from src.modules.events.models import *
from src.modules.bets.models import *

from src.dependencies.session import get_session


ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
SessionMaker = sessionmaker(   # type: ignore
    async_engine, autoflush=False, class_=AsyncSession, expire_on_commit=False
)


async def get_sqlite_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionMaker() as session:
        yield session


@pytest.fixture(scope="function")
async def sqlite_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        async with SessionMaker() as session:
            yield session
        await conn.run_sync(BaseModel.metadata.drop_all)


app.dependency_overrides[get_session] = get_sqlite_session  # type: ignore


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)
