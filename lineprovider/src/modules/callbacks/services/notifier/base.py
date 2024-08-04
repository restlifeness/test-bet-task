
from typing import Any
from abc import ABC, abstractmethod


class AbstractNotifier(ABC):
    @abstractmethod
    async def notify(self, receiver: Any) -> Any:
        """Notify a receiver about a change."""
        ...
