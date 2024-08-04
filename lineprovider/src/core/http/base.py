
from abc import ABC, abstractmethod
from typing import Any


class BaseHttpClient:
    @abstractmethod
    async def get(
        self,
        url: str,
        params: dict[str, str | Any] | None = None,
        headers: dict[str, str | Any] | None = None,
    ) -> Any:
        """GET Request to url"""
        ...

    @abstractmethod
    async def post(
        self,
        url: str,
        body: dict[str, str | Any] | None = None,
        headers: dict[str, str | Any] | None = None,
    ) -> Any:
        """POST Request to url"""
        ...
