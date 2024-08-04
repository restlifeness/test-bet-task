
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

    def _update_from_data(
        self,
        model: T,
        data: BaseSchemaModel,
        exclude_unset: bool = False,
        exclude: list[str] | None = None
   ) -> T:
        """
        Updates event data from event data.

        :param model: SQLAlchemy object to update
        :param data: Schema data to update
        :param exclude_unset: Exclude unset keys from data
        :return: Updated object
        """
        return self.repo.update_model_from_data(
            model,
            data.model_dump(exclude=exclude, exclude_unset=exclude_unset),
            exclude_unset
        )
