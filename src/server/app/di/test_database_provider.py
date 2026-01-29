from collections.abc import AsyncGenerator
from typing import Any

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession


class TestDatabaseProvider(Provider):
    """Провайдер для внедрения сессий базы данных в тестовом окружении."""

    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncGenerator[AsyncSession, Any]:
        yield self._session
