from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import User
from ..inputs import UserAddInput


class UserRepository:
    @staticmethod
    async def get_user_by_discord_id(
        session: AsyncSession, discord_id: int
    ) -> User | None:
        result = await session.execute(
            select(User).where(User.discord_id == discord_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    def get_users_query():
        return select(User).order_by(User.id)

    @staticmethod
    async def add_users(session: AsyncSession, users: list[UserAddInput]) -> list[User]:
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
