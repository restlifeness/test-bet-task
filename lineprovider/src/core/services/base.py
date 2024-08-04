import typing

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


if typing.TYPE_CHECKING:
    from ..repositories.generic import Repository


class SimpleService:
    pass


class AsyncSessionService:
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize session service.

        :param session: async session
        """
        if not isinstance(session, AsyncSession):
            raise ValueError('session must be an instance of AsyncSession')

        self.session = session
        self.repo: Repository | None = None

        self.post_init()

    def post_init(self) -> None:
        """
        Called after service initialization.
        """
        pass


class CRUDService(AsyncSessionService):
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize CRUD service.

        :param session: async session
        """
        super().__init__(session)
        raise NotImplementedError('Work in progress...')

    """
    WIP: add CRUD methods
    """
