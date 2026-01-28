from httpx import AsyncClient

from .base_http_client import BaseHttpClient


class HttpxTestsClient(BaseHttpClient):
    """
    Асинхронный HTTP-клиент на основе httpx для тестирования ASGI приложений.
    Используется для взаимодействия с тестовым сервером.
    Реализация HTTP-клиента для тестового окружения.
    Имплементирует общий интерфейс HttpClient.
    Используется с асинхронным контекстным менеджером.
    """

    def __init__(self, client: AsyncClient):
        self.client = client

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass  # lifecycle управляется фикстурой

    async def get(self, path: str, **kwargs):
        resp = await self.client.get(path, **kwargs)
        resp.raise_for_status()
        return resp.json()

    async def post(self, path: str, **kwargs):
        resp = await self.client.post(path, **kwargs)
        resp.raise_for_status()
        return resp.json()

    async def put(self, path: str, **kwargs):
        resp = await self.client.put(path, **kwargs)
        resp.raise_for_status()
        return resp.json()

    async def delete(self, path: str, **kwargs):
        resp = await self.client.delete(path, **kwargs)
        resp.raise_for_status()
        return resp.json()
