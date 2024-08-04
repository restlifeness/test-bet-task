
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel as BaseSchemaModel

from src.database.models import BaseModel
from src.core.repositories.generic import Repository


T = TypeVar('T', bound=BaseModel)


class AsyncSessionService(Generic[T]):
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize session service.

        :param session: async session
        """
        if not isinstance(session, AsyncSession):
            raise ValueError('session must be an instance of AsyncSession')

        self.session = session
        self.repo: Repository | None = None

        self.__post_init__()

    def __post_init__(self) -> None:
        """
        Called after service initialization.
        """
        pass
