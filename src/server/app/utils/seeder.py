from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ....shared import StructuredLogger
from ..db.models import User
from ..inputs import UserAddInput
from ..repositories import UserRepository


class Seeder:
    """Класс для заполнения и очистки базы данных начальными данными."""

    @staticmethod
    async def seed(session: AsyncSession) -> bool:
        """Заполняет базу данных начальными данными."""
        users_to_add = []
        for i in range(15):
            user_input = UserAddInput(
                discord_id=7373 + i * 73,
                username=f"user_{i * 37}",
                avatar_url=f"https://placehold.co/73x37?text=user_{i * 37}",
            )
            users_to_add.append(user_input)
        try:
            await UserRepository.add_users(session=session, users=users_to_add)
            return True
        except Exception:
            await session.rollback()
            StructuredLogger.exception("Error seeding database")
            return False

    @staticmethod
    async def clear(session: AsyncSession):
        """Очищает базу данных."""
        await session.execute(delete(User))
        await session.flush()
