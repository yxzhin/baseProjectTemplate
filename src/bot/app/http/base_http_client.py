from typing import Any, Protocol


class BaseHttpClient(Protocol):
    """
    Общий интерфейс HTTP-клиента.
    Используется для обеспечения совместимости между разными реализациями HTTP-клиентов.
    Имплементируется AiohttpClient и HttpxTestsClient.
    """

    async def get(self, path: str, **kwargs) -> Any: ...
    async def post(self, path: str, **kwargs) -> Any: ...
    async def put(self, path: str, **kwargs) -> Any: ...
    async def delete(self, path: str, **kwargs) -> Any: ...
