from typing import Sequence

from src.core.repositories import Repository
from src.core.services import AsyncSessionService
from src.core.mapper import SchemaToDatabaseMapper
from src.modules.events.handlers import EventStatusHandler
from src.modules.callbacks.jobs import send_update_to_subscribers
from src.common.decorators import return_side_effect

from src.modules.events.models import Event

from src.api.v1.events.schemas import (
    EventCreate,
    EventUpdate,
    EventPatch,
)


class EventsService(AsyncSessionService[Event]):
    mapper: SchemaToDatabaseMapper

    def __post_init__(self) -> None:
        self.repo = Repository(Event, self.session)
        self.mapper = SchemaToDatabaseMapper()

    @return_side_effect(send_update_to_subscribers.send, attr='id', skip_on_tests=True)
    async def create(self, event_data: EventCreate) -> Event:
        """Creates a new event."""
        return await self.repo.create(Event(**event_data.model_dump()))

    @return_side_effect(send_update_to_subscribers.send, attr='id', skip_on_tests=True)
    async def update(self, event: Event, event_data: EventUpdate) -> Event:
        """Updates an existing event"""

        updated_event = self.mapper.map(
            event_data,
            event,
            exclude={'status'},
        )

        # NOTE: Manually handled status for event
        EventStatusHandler(event).set_status(event_data.status)

        await self.repo.save()

        return updated_event

    @return_side_effect(send_update_to_subscribers.send, attr='id', skip_on_tests=True)
    async def patch(self, event: Event, event_data: EventPatch) -> Event:
        """Patches a existing event."""

        updated_event = self.mapper.map(
            event_data,
            event,
            exclude_unset=True,
            exclude={'status'},
        )

        # NOTE: Manually handled status for event
        if event_data.status:
            EventStatusHandler(updated_event).set_status(event_data.status)

        await self.repo.save()

        return updated_event

    async def get_by_id(self, event_id: int) -> Event | None:
        """Gets an existing event."""
        return await self.repo.get_by_id(event_id)

    async def get_all(self) -> Sequence[Event]:
        """Gets all existing events."""
        return await self.repo.all()
