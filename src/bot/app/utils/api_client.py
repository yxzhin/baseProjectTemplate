from typing import Any

from aiohttp import ClientSession, ClientTimeout, ContentTypeError

from ....shared import StructuredLogger
from ..conf import Config


class APIClient:
    def __init__(self, timeout: int = 10):
        self.base_url = Config.API_URL.rstrip("/")
        self.timeout = ClientTimeout(total=timeout)
        self.session: ClientSession | None = None

    async def start(self):
        if not self.session or self.session.closed:
            self.session = ClientSession(timeout=self.timeout)

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        if not self.session:
            await self.start()
        url = f"{self.base_url}{path}"
        async with self.session.request(  # type: ignore
            method, url, params=params, json=json, data=data, headers=headers
        ) as resp:
            # выбрасываем исключение при ошибке
            resp.raise_for_status()
            # пытаемся вернуть JSON, если нет — текст
            result = None
            try:
                result = await resp.json()
                return result
            except ContentTypeError:
                result = await resp.text()
                return result
            finally:
                StructuredLogger.info(
                    "[api]",
                    method=method,
                    url=url,
                    status=resp.status,
                    result=result,
                    params=params,
                    json=json,
                    data=data,
                    headers=headers,
                )

    async def get(self, path: str, **kwargs):
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs):
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs):
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs):
        return await self._request("DELETE", path, **kwargs)

    # Для использования с async with
    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
