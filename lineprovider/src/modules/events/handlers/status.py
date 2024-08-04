
from src.modules.events.models import Event
from src.modules.events.enums import EventStatus
from src.modules.events.exceptions import EventStatusSetError

from .base import BaseEventHandler


class EventStatusHandler(BaseEventHandler):
    def set_status(self, status: EventStatus) -> Event:
        """
        Sets the status of the event.

        :param status: The status of the event.
        :return: Updated event.
        """

        if status in self.event.open_statuses and self.event.is_ended():
            raise EventStatusSetError("Can not set open status for outdated events")

        self.event.status = status

        return self.event
