
from src.modules.events.models import Event


class BaseEventHandler:
    def __init__(self, event: Event) -> None:
        """
        Initialize the event handler for :class:`Event` model.

        :param event: Event object
        """

        self.event = event
