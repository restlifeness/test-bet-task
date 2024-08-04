
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Sequence

from src.core.repositories import Repository
from src.common.time import utc_now

from src.modules.events.models import ExternalEvent
from src.modules.events.enums import ExternalEventStatus


class ExternalEventsRepository(Repository[ExternalEvent]):
    async def get_active_external_events(
        self,
        offset: int = 0,
        limit: int = 30,
    ) -> Sequence[ExternalEvent]:
        query = (
            select(ExternalEvent)
            .where(
                ExternalEvent.status == ExternalEventStatus.OPEN,
                ExternalEvent.deadline > utc_now(),
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_from_external_event_id(
        self,
        external_event_id: int,
        load_bets: bool = False,
    ) -> ExternalEvent | None:
        """"""
        query = (
            select(ExternalEvent)
            .where(ExternalEvent.external_id == external_event_id)
        )

        if load_bets:
            query = query.options(selectinload(ExternalEvent.bets))

        result = await self.session.execute(query)

        return result.scalars().one_or_none()
