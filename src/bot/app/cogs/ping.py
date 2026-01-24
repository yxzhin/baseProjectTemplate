from discord import Interaction, app_commands
from discord.ext.commands import Bot, Cog


class Ping(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="test bot latency")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(
            f"`pong! latency: ~{self.bot.latency}s`"
        )


async def setup(bot: Bot):
    await bot.add_cog(Ping(bot))
