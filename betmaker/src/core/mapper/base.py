
from abc import ABC, abstractmethod
from typing import Any


class AbstractMapper(ABC):
    @abstractmethod
    def map(self, first: Any, second: Any) -> Any:
        """Map first object to second."""
        ...
