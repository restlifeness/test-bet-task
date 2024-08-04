import logging
from typing import Sequence

from src.core.services import AsyncSessionService

from src.modules.events.models import Event

from src.modules.subscribers.models import UpdateSubscriber
from src.modules.subscribers.services.subscribers import SubscribersService
from src.modules.callbacks.services.notifier import EventUpdateNotifierService


class CallbackEventUpdatesService(AsyncSessionService):
    subscribers_service: SubscribersService

    def __post_init__(self) -> None:
        self.subscribers_service = SubscribersService(self.session)

    async def notify_event_updates(self, event: Event) -> None:
        """Notify all subscribers about an event update."""
        subscribers: Sequence[UpdateSubscriber] = await self.subscribers_service.get_all_active_subscribers()

        await EventUpdateNotifierService(event).notify_all(subscribers)
