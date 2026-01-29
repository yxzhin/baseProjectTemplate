from collections.abc import AsyncGenerator
from typing import Any

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import Database
from ..repositories import UserRepository
from ..services import UserService


class AppProvider(Provider):
    """
    Провайдер для внедрения зависимостей в приложение.
    Предоставляет сессии базы данных, репозитории и сервисы.
    """

    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncGenerator[AsyncSession, Any]:
        """
        Предоставляет асинхронную сессию базы данных для каждого запроса.
        Используется внутри контекстного менеджера async with.
        """
        async with Database.get_session() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def user_repo(self, session: AsyncSession) -> UserRepository:
        """Предоставляет репозиторий пользователей, используя сессию базы данных."""
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def user_service(self, repo: UserRepository) -> UserService:
        """Предоставляет сервис пользователей, используя репозиторий пользователей."""
        return UserService(repo)
