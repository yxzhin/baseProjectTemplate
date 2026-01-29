from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import User


class UserRepository:
    """Репозиторий для управления операциями с пользователями в базе данных."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_discord_id(self, discord_id: int) -> User | None:
        """Получает пользователя по его Discord ID."""
        result = await self.session.execute(
            select(User).where(User.discord_id == discord_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """Получает пользователя по его имени пользователя."""
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_users(self, offset: int = 0, limit: int = 10) -> Sequence[User]:
        """Получает список пользователей с поддержкой пагинации."""
        result = await self.session.execute(select(User).offset(offset).limit(limit))
        return result.scalars().all()

    async def create_user(
        self, discord_id: int, username: str, avatar_url: str | None = None
    ) -> User:
        """Создает нового пользователя в базе данных."""
        new_user = User(
            discord_id=discord_id,
            username=username,
            avatar_url=avatar_url,
        )
        self.session.add(new_user)
        await self.session.flush()
        return new_user
