from discord import Interaction, app_commands
from discord.ext.commands import Bot, Cog

from ..utils import APIClient


class ApiTest(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="api_test", description="test the fastapi app")
    async def api_test(self, interaction: Interaction):
        async with APIClient() as api_client:
            result = await api_client.get("/test")
        await interaction.response.send_message(f"`{result}`")


async def setup(bot: Bot):
    await bot.add_cog(ApiTest(bot))
