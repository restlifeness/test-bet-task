
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import ASYNC_SESSION


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async session."""
    async with ASYNC_SESSION() as session:
        yield session
