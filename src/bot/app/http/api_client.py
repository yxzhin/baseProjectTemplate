from . import AiohttpClient
from .base_http_client import BaseHttpClient


class APIClient:
    """
    Универсальный HTTP-клиент для взаимодействия с внешним API.
    Может использоваться с разными реализациями HTTP-клиентов.
    По умолчанию использует AiohttpClient.
    Имплементирует общий интерфейс HttpClient.
    Используется с асинхронным контекстным менеджером.
    """

    def __init__(self, http_client: BaseHttpClient | None = None):
        self._external = http_client
        self._client: BaseHttpClient | None = None

    async def __aenter__(self):
        if self._external:
            self._client = self._external
        else:
            self._client = AiohttpClient()
            await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if not self._external and self._client:
            await self._client.__aexit__(exc_type, exc, tb)  # pyright: ignore[reportAttributeAccessIssue]

    async def get(self, path: str):
        if not self._client:
            raise RuntimeError("client not initialized. use async with to initialize.")
        return await self._client.get(path)

    async def post(self, path: str, json: dict):
        if not self._client:
            raise RuntimeError("client not initialized. use async with to initialize.")
        return await self._client.post(path, json=json)

    async def put(self, path: str, json: dict):
        if not self._client:
            raise RuntimeError("client not initialized. use async with to initialize.")
        return await self._client.put(path, json=json)

    async def delete(self, path: str):
        if not self._client:
            raise RuntimeError("client not initialized. use async with to initialize.")
        return await self._client.delete(path)
