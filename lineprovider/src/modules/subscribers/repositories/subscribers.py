
from typing import Sequence

from sqlalchemy import select

from src.core.repositories import Repository
from src.modules.subscribers.models import UpdateSubscriber
from src.modules.subscribers.enums import SubscriberStatus


class SubscribersRepository(Repository[UpdateSubscriber]):

    async def get_all_active_subscribers(self) -> Sequence[UpdateSubscriber]:
        """Get all active subscribers."""

        query = (
            select(UpdateSubscriber)
            .where(UpdateSubscriber.status == SubscriberStatus.ACTIVE)
            .order_by(UpdateSubscriber.id)
        )

        result = await self.session.execute(query)
        return result.scalars().all()
