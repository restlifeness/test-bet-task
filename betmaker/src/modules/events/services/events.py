
from typing import Sequence

from src.core.services import AsyncSessionService
from src.modules.events.repositories import ExternalEventsRepository

from src.modules.events.models import ExternalEvent


class ExternalEventsService(AsyncSessionService):

    def __post_init__(self) -> None:
        self.repo = ExternalEventsRepository(ExternalEvent, self.session)

    async def get_active_external_events(
        self,
        offset: int,
        limit: int,
    ) -> Sequence[ExternalEvent]:
        """Get active external events."""
        return await self.repo.get_active_external_events(offset, limit)

    async def get_by_id(self, id: int) -> ExternalEvent:
        """Get external event by id."""
        return await self.repo.get_by_id(id)
