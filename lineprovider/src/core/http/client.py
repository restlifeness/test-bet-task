from typing import Any
from aiohttp import ClientSession, ClientResponse, ClientTimeout

from .base import BaseHttpClient


class HttpClient(BaseHttpClient):
    def __init__(
        self,
        timeout: float = 10,
    ) -> None:
        self.session = ClientSession(timeout=ClientTimeout(total=timeout))

    async def get(
        self,
        url: str,
        params: dict[str, str | Any] | None = None,
        headers: dict[str, str | Any] | None = None,
    ) -> dict[str, Any]:
        async with self.session.get(url, params=params, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def post(
        self,
        url: str,
        body: dict[str, str | Any] | None = None,
        headers: dict[str, str | Any] | None = None,
    ) -> dict[str, Any]:
        async with self.session.post(url, json=body, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def close(self) -> None:
        """Close the client session."""
        await self.session.close()
