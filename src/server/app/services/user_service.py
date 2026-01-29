from collections.abc import Sequence

from ..db.models import User
from ..inputs import UserCreateInput
from ..repositories import UserRepository


class UserService:
    """
    Сервис для управления логикой пользователей.
    Использует UserRepository для взаимодействия с базой данных.
    """

    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user_by_discord_id(self, discord_id: int) -> User | None:
        """Получает пользователя по его Discord ID."""
        return await self.repo.get_user_by_discord_id(discord_id)

    async def get_user_by_username(self, username: str) -> User | None:
        """Получает пользователя по его имени пользователя."""
        return await self.repo.get_user_by_username(username)

    async def get_users(self, page: int = 1, limit: int = 10) -> Sequence[User]:
        """Получает список пользователей с поддержкой пагинации."""
        offset = (page - 1) * limit
        return await self.repo.get_users(offset=offset, limit=limit)

    async def create_user(self, user: UserCreateInput) -> User:
        """Создает нового пользователя."""
        return await self.repo.create_user(
            discord_id=user.discord_id,
            username=user.username,
            avatar_url=user.avatar_url,
        )

    async def create_users(self, users: list[UserCreateInput]) -> list[User]:
        """Создает нескольких пользователей."""
        created_users = []
        for user in users:
            created_user = await self.create_user(user)
            created_users.append(created_user)
        return created_users
