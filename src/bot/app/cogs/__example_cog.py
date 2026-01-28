from discord import Interaction, app_commands
from discord.ext.commands import Bot, Cog


class ExampleCog(Cog):
    """Пример кога для демонстрации структуры."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="example", description="example command")
    async def example(self, interaction: Interaction):
        await interaction.response.send_message("sample text")


async def setup(bot: Bot):
    await bot.add_cog(ExampleCog(bot))
