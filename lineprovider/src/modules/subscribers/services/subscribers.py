from typing import Sequence

from src.core.services import AsyncSessionService
from src.core.mapper import SchemaToDatabaseMapper

from src.api.v1.subscribers.schemas import UpdateSubscriberCreate, UpdateSubscriberUpdate
from src.modules.subscribers.repositories import SubscribersRepository
from src.modules.subscribers.models import UpdateSubscriber


class SubscribersService(AsyncSessionService):
    mapper: SchemaToDatabaseMapper

    def __post_init__(self) -> None:
        self.repo = SubscribersRepository(UpdateSubscriber, self.session)
        self.mapper = SchemaToDatabaseMapper()

    async def get_all_active_subscribers(self) -> Sequence[UpdateSubscriber]:
        """Get all active subscribers."""
        return await self.repo.get_all_active_subscribers()

    async def get_by_id(self, _id: int) -> UpdateSubscriber:
        """Get subscriber by id."""
        return await self.repo.get_by_id(_id)

    async def create(self, data: UpdateSubscriberCreate) -> UpdateSubscriber:
        """Create subscriber from data"""
        return await self.repo.create(UpdateSubscriber(**data.model_dump()))

    async def put(self, record: UpdateSubscriber, data: UpdateSubscriberUpdate) -> UpdateSubscriber:
        """Update subscriber from data"""
        record = self.mapper.map(data, record)
        await self.repo.save()

        return record
