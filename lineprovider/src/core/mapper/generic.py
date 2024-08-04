
from typing import TypeVar, Generic, Any

from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

from .base import AbstractMapper


S = TypeVar('S', bound=BaseModel)
M = TypeVar('M', bound=DeclarativeBase)


class SchemaToDatabaseMapper(AbstractMapper, Generic[M, S]):
    def __init__(self, custom_mapping: dict[str, str] | None = None) -> None:
        """
        :param custom_mapping: Custom mapping for
        """
        self.custom_mapping: dict[str, str] | None = custom_mapping

    def _get_real_key(self, k: str) -> str:
        """Get real object key"""
        if not self.custom_mapping:
            return k

        if k not in self.custom_mapping:
            raise ValueError(f'Custom mapping in SchemaToDatabaseMapper has not custom key for key={k}')

        return self.custom_mapping[k]

    def map(
        self,
        first: S,
        second: M,
        exclude: set[str] | None = None,
        exclude_unset: bool = False,
    ) -> M:
        """
        Map from pydantic model to SQLAlchemy model.

        :param first: Schema model
        :param second: SQLAlchemy model
        :param exclude: set of keys to exclude
        :param exclude_unset: bool to exclude unset keys
        :return: updated SQLAlchemy model
        """
        data: dict[str, Any] = first.model_dump(exclude=exclude, exclude_unset=exclude_unset)

        for k, v in data.items():
            # NOTE: if custom_mapping is unset, real_key = original key
            _real_key = self._get_real_key(k)

            if not hasattr(second, _real_key):
                raise ValueError(f'Key key={_real_key} has not mapping for {type(second)} in second!')

            setattr(second, _real_key, v)

        return second
