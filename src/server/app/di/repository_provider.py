from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories import UserRepository


class RepositoryProvider(Provider):
    """Провайдер для внедрения репозиториев в приложение."""

    @provide(scope=Scope.REQUEST)
    def user_repo(self, session: AsyncSession) -> UserRepository:
        """Предоставляет репозиторий пользователей, используя сессию базы данных."""
        return UserRepository(session)
