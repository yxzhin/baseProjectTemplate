from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import User
from ..inputs import UserAddInput


class UserRepository:
    """Репозиторий для управления операциями с пользователями в базе данных."""

    @staticmethod
    async def get_user_by_discord_id(
        session: AsyncSession, discord_id: int
    ) -> User | None:
        """Получает пользователя по его Discord ID."""
        result = await session.execute(
            select(User).where(User.discord_id == discord_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
        """Получает пользователя по его имени пользователя."""
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    def get_users_query():
        """Возвращает запрос для получения всех пользователей, отсортированных по ID."""
        return select(User).order_by(User.id)

    @staticmethod
    async def add_users(session: AsyncSession, users: list[UserAddInput]) -> list[User]:
        """Добавляет несколько пользователей в базу данных."""
        new_users = []
        for user in users:
            new_user = User(
                discord_id=user.discord_id,
                username=user.username,
                avatar_url=user.avatar_url,
            )
            new_users.append(new_user)
        session.add_all(new_users)
        await session.flush()
        return new_users
