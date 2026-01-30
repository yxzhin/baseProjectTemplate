from ..inputs import BotUserCreateInput
from ..models import BotUser
from ..repositories import BotUserRepository


class BotUserService:
    def __init__(self, bot_user_repository: BotUserRepository):
        self.bot_user_repository = bot_user_repository

    async def get_bot_user_by_discord_id(self, discord_id: int) -> BotUser | None:
        return await self.bot_user_repository.get_bot_user_by_discord_id(
            discord_id=discord_id
        )

    async def get_bot_user_by_username(self, username: str) -> BotUser | None:
        return await self.bot_user_repository.get_bot_user_by_username(
            username=username
        )

    async def get_bot_users(self, page: int = 1, limit: int = 10) -> list[BotUser]:
        return await self.bot_user_repository.get_bot_users(page=page, limit=limit)

    async def create_bot_user(self, bot_user: BotUserCreateInput) -> BotUser | None:
        return await self.bot_user_repository.create_bot_user(bot_user=bot_user)

    async def create_bot_users(
        self, bot_users: list[BotUserCreateInput]
    ) -> list[BotUser | None]:
        created_bot_users = []
        for bot_user in bot_users:
            created_bot_user = await self.create_bot_user(bot_user)
            created_bot_users.append(created_bot_user)
        return created_bot_users

    async def get_or_create_bot_user(self, bot_user: BotUserCreateInput) -> BotUser:
        get_bot_user = await self.get_bot_user_by_discord_id(
            discord_id=bot_user.discord_id,
        )
        if get_bot_user:
            return get_bot_user
        return await self.create_bot_user(bot_user=bot_user)  # type: ignore
