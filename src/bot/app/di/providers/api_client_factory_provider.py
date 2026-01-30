from collections.abc import AsyncGenerator
from typing import Any

from dishka import Provider, Scope, provide

from ...http import APIClient


class APIClientFactoryProvider(Provider):
    def __init__(self, api_client_factory: type[APIClient] = APIClient):
        super().__init__()
        self._api_client_factory = api_client_factory

    @provide(scope=Scope.REQUEST)
    async def api_client_factory(self) -> AsyncGenerator[type[APIClient], Any]:
        yield self._api_client_factory
