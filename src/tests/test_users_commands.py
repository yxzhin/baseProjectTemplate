from dishka import Scope

from src.bot.app.cogs import UserCog
from src.bot.app.inputs import BotUserCreateInput
from src.bot.app.services import BotUserService


async def test_user_profile_command(bot, bot_container):
    async with bot_container(scope=Scope.REQUEST) as test_container:
        bot_user_service = await test_container.get(BotUserService)
    bot_user = BotUserCreateInput(
        discord_id=7373,
        username="test7373",
        avatar_url="https://placehold.co/73x37",
    )
    response = await UserCog(bot).profile(
        bot_user=bot_user,
        bot_user_service=bot_user_service,
    )
    assert "it works!! :tada:" in response
