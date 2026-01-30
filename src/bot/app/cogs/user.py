from discord import Interaction, app_commands
from discord import User as DiscordUser
from discord.ext.commands import Cog

from .. import TheBot
from ..di import inject, with_di
from ..inputs import BotUserCreateInput
from ..services import BotUserService


class UserCog(Cog):
    def __init__(self, bot: TheBot):
        self.bot = bot

    @inject
    async def profile(
        self,
        bot_user: BotUserCreateInput,
        bot_user_service: BotUserService,
    ) -> str:
        get_bot_user = await bot_user_service.get_or_create_bot_user(bot_user=bot_user)
        return f"it works!! :tada:\n`balance: {get_bot_user.balance:,}`"

    @app_commands.command(name="profile", description="shows profile of the user")
    @with_di
    async def _profile(
        self,
        interaction: Interaction,
        user: DiscordUser | None = None,
    ):
        if user is None:
            user = interaction.user  # type: ignore
        bot_user = BotUserCreateInput(
            discord_id=user.id,  # type: ignore
            username=user.name,  # type: ignore
            avatar_url=user.avatar.url if user.avatar is not None else None,  # type: ignore
        )
        await interaction.response.send_message(await self.profile(bot_user=bot_user))  # pyright: ignore[reportCallIssue]


async def setup(bot: TheBot):
    await bot.add_cog(UserCog(bot))
