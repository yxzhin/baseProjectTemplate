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
    async def add_user(session: AsyncSession, user: UserAddInput) -> User:
        new_user = User(
            discord_id=user.discord_id,
            username=user.username,
            avatar_url=user.avatar_url,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
