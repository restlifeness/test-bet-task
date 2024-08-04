
from abc import ABC, abstractmethod


class AbstractRequestor(ABC):
    @abstractmethod
    async def request(self, ):
