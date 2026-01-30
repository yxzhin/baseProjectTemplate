from pydantic import TypeAdapter

from ..http import APIClient
from ..inputs import BotUserCreateInput
from ..models import BotUser


class BotUserRepository:
    def __init__(self, api_client_factory: type[APIClient]):
        self.api_client_factory = api_client_factory

    async def get_bot_user_by_discord_id(self, discord_id: int) -> BotUser | None:
        async with self.api_client_factory() as api_client:
            result = await api_client.get(f"/users/{discord_id}")
        if result is None or result["success"] is False:
            return None
        bot_user = BotUser.model_validate(result["user"])
        return bot_user

    async def get_bot_user_by_username(self, username: str) -> BotUser | None:
        async with self.api_client_factory() as api_client:
            result = await api_client.get(f"/users/username/{username}")
        if result is None or result["success"] is False:
            return None
        bot_user = BotUser.model_validate(result["user"])
        return bot_user

    async def get_bot_users(self, page: int = 1, limit: int = 10) -> list[BotUser]:
        async with self.api_client_factory() as api_client:
            result = await api_client.get(f"/users/?page={page}&limit={limit}")
        if result is None or result["success"] is False:
            return []
        bot_users_adapter = TypeAdapter(list[BotUser])
        bot_users = bot_users_adapter.validate_python(result["users"])
        return bot_users

    async def create_bot_user(self, bot_user: BotUserCreateInput) -> BotUser | None:
        json = bot_user.model_dump()
        async with self.api_client_factory() as api_client:
            result = await api_client.post("/users/add", json=json)
        if result["success"] is False:
            return None
        new_bot_user = BotUser.model_validate(result["user"])
        return new_bot_user
