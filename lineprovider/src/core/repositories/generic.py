
from typing import Type, TypeVar, Generic, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .base import BaseRecordOrientedRepository


T = TypeVar('T', bound=DeclarativeBase)


class Repository(BaseRecordOrientedRepository, Generic[T]):

    def __init__(self, model: Type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(
            self,
            _id: int,
            options: list | None = None,
    ) -> T | None:
        """
        Get record by id, return None if not found.

        :param _id: record id to get
        :param options: SQLAlchemy options for query
        :return: record or None
        """
        query = (
            select(self.model)
            .where(self.model.id == _id)
        )

        if options:
            query = query.options(*options)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def all(self, options: list | None = None) -> Sequence[T]:
        """
        Get all records.

        :param options: SQLAlchemy options for query
        :return: list of records
        """
        query = select(self.model)

        if options:
            query = query.options(**options)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def create(self, record: T, with_commit: bool = True) -> T:
        """
        Create record.

        :param record: record
        :param with_commit: commit after insert
        :return: record
        """
        self.session.add(record)
        await self.session.flush()

        if with_commit:
            await self.session.commit()

        return record

    async def update(self, record: T, with_commit: bool = True) -> T:
        """
        Update record.

        :param record: record
        :param with_commit: commit after update
        :return: record
        """
        await self.session.merge(record)
        await self.session.flush()

        if with_commit:
            await self.session.commit()

        return record

    async def delete(self, record: T, with_commit: bool = True) -> None:
        """
        Delete record.

        :param record: record
        :param with_commit: commit after delete
        :return: record
        """
        await self.session.delete(record)
        await self.session.flush()

        if with_commit:
            await self.session.commit()

    async def filter_by(
        self,
        options: list | None = None,
        use_list: bool = True,
        order_by: list | None = None,
        **kwargs,
    ) -> T | Sequence[T]:
        query = (
            select(self.model)
            .filter_by(**kwargs)
        )

        if options is not None:
            query = query.options(*options)

        if order_by is not None:
            query = query.order_by(*order_by)

        result = await self.session.execute(query)

        if not use_list:
            return result.scalars().first()

        return result.scalars().all()

    async def save(self):
        await self.session.commit()
