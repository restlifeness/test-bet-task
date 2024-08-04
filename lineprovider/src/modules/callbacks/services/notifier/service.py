from typing import Any, Sequence

from src.modules.events.models import Event
from src.modules.subscribers.models import UpdateSubscriber
from src.modules.callbacks.utils.requestor import Requestor
from src.api.v1.events.schemas import EventResponse

from .base import AbstractNotifier


class EventUpdateNotifierService(AbstractNotifier):
    def __init__(self, event: Event) -> None:
        self.event = event

    def _prepare_body(self) -> dict[str, Any]:
        """Validate event record to dict"""
        return EventResponse.model_validate(self.event, from_attributes=True).model_dump(mode='json')

    async def notify(self, receiver: UpdateSubscriber) -> bool:
        url: str = receiver.callback_url
        body: dict[str, Any] = self._prepare_body()

        async with Requestor() as requestor:
            result = await requestor.post(url, body)

        return bool(result)

    async def notify_all(self, receivers: list[UpdateSubscriber] | Sequence[UpdateSubscriber]) -> bool:
        urls: list[str] = [rec.callback_url for rec in receivers]
        body: dict[str, Any] = self._prepare_body()

        async with Requestor() as requestor:
            results = await requestor.many_post(urls, body=body)

        return all(results)
