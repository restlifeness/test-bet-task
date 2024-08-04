import asyncio
from asyncio import Semaphore
from typing import Literal, Any

from src.core.http import HttpClient, BaseHttpClient


class Requestor(BaseHttpClient):
    def __init__(
        self,
        max_requests: int = 10,
        timeout: float = 10,
        custom_client: HttpClient | BaseHttpClient | None = None,
    ) -> None:
        """
        Async requestor

        :param max_requests: max number of requests allowed
        :param timeout: timeout in seconds
        :param custom_client: Custom HTTP client
        """
        self._client = custom_client or HttpClient(timeout=timeout)
        self._semaphore = Semaphore(max_requests)

    async def __aenter__(self) -> "Requestor":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._client.close()

    async def post(
        self,
        url: str,
        body: dict[str, str | Any] | None = None,
        headers: dict[str, str | Any] | None = None,
    ) -> dict[str, Any]:
        """
        Asyncio Semaphore controlled POST request

        :param url: URL to POST
        :param body: body of the request
        :param headers: headers of the request
        :return: response body
        """
        async with self._semaphore:
            return await self._client.post(
                url=url,
                body=body,
                headers=headers,
            )

    async def get(
        self,
        url: str,
        params: dict[str, str | Any] | None = None,
        headers: dict[str, str | Any] | None = None,
    ) -> dict[str, Any]:
        """
        Asyncio Semaphore controlled GET request

        :param url: URL to GET
        :param params: parameters of the request
        :param headers: headers of the request
        :return: response body
        """
        async with self._semaphore:
            return await self._client.get(
                url=url,
                params=params,
                headers=headers,
            )

    async def many_post(
        self,
        urls: list[str],
        body: dict[str, str | Any] | None = None,
        headers: dict[str, str | Any] | None = None
    ) -> tuple[dict[str, Any] | BaseException]:
        """
        POST Request many urls with same params

        :param urls: urls to POST
        :param body: body of the request
        :param headers: headers of the request
        :return: response bodies
        """
        _coroutines = [
            self.post(url, body, headers)
            for url in urls
        ]

        return await asyncio.gather(*_coroutines, return_exceptions=False)
