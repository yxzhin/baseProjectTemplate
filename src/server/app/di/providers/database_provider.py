from collections.abc import AsyncGenerator
from typing import Any

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import Database


class DatabaseProvider(Provider):
    """Провайдер для внедрения сессий базы данных в Production-среде."""

    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncGenerator[AsyncSession, Any]:
        """
        Предоставляет асинхронную сессию базы данных для каждого запроса.
        Используется внутри контекстного менеджера async with.
        """
        async with Database.get_session() as session:
            yield session
