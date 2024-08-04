
from abc import ABC, abstractmethod
from typing import Any, Sequence


class BaseRecordOrientedRepository(ABC):
    @abstractmethod
    async def get_by_id(self, _id: int) -> Any | None:
        """Get record by id"""
        ...

    @abstractmethod
    async def all(self) -> Sequence[Any]:
        """Get all records"""
        ...

    @abstractmethod
    async def create(self, record: Any) -> Any:
        """Create record"""
        ...

    @abstractmethod
    async def update(self, record: Any) -> Any:
        """Update record"""
        ...

    @abstractmethod
    async def delete(self, record: Any) -> Any:
        """Delete record"""
        ...
