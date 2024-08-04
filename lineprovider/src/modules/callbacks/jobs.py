import dramatiq
import logging

from src.database.connection import SessionMaker
from src.core.repositories import Repository
from src.modules.callbacks.services.callbacks import CallbackEventUpdatesService

from src.modules.events.models import Event


log = logging.getLogger(__name__)


@dramatiq.actor
async def send_update_to_subscribers(event_id: int):
    async with SessionMaker() as session:
        event: Event | None = await Repository(Event, session).get_by_id(event_id)

        if not event:
            log.warning(f"Event id={event_id} not found in job send_update_to_subscribers!")
            return

        await CallbackEventUpdatesService(session).notify_event_updates(event)
