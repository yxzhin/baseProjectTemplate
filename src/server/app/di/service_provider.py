from dishka import Provider, Scope, provide

from ..repositories import UserRepository
from ..services import UserService


class ServiceProvider(Provider):
    """Провайдер для внедрения сервисов в приложение."""

    @provide(scope=Scope.REQUEST)
    def user_service(self, repo: UserRepository) -> UserService:
        """Предоставляет сервис пользователей, используя репозиторий пользователей."""
        return UserService(repo)
