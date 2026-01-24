from os.path import dirname, realpath
from sys import argv

from discord import Interaction
from discord.app_commands import command, describe
from discord.ext.commands import Cog, is_owner

from ....shared import StructuredLogger
from .. import TheBot
from ..utils import get_extension_path


class Reload(Cog):
    def __init__(self, bot: TheBot):
        self.bot = bot

    @command(name="reload", description="reload a cog")
    @describe(cog="target cog filename (ex. ping)")
    @is_owner()
    async def reload(self, interaction: Interaction, cog: str):
        try:
            abs_cogs_path = dirname(realpath(argv[0])) + "/cogs"
            file = f"{cog}.py"
            cog_path = get_extension_path(abs_cogs_path, file)
            await self.bot.reload_extension(cog_path)
            await self.bot.tree.sync(guild=interaction.guild)
            await interaction.response.send_message(
                f":white_check_mark: cog `{cog}` reloaded successfully"
            )
            StructuredLogger.info(f"[bot] reloaded cog: {cog}")

        except Exception as e:
            StructuredLogger.exception(f"[bot] error while reloading cog: {cog}")
            await interaction.response.send_message(
                f":x: an error occurred:\n```{e}```", ephemeral=True
            )

    @command(name="reload_all", description="reload all cogs")
    @is_owner()
    async def reload_all(self, interaction: Interaction):
        failed = await self.bot.load_all_cogs(reload_=True)
        await self.bot.tree.sync(guild=interaction.guild)

        if failed:
            await interaction.response.send_message(
                ":x: some errors occurred:\n" + "\n".join(failed), ephemeral=True
            )
            return

        await interaction.response.send_message(
            ":white_check_mark: all cogs reloaded successfully"
        )


async def setup(bot: TheBot):
    await bot.add_cog(Reload(bot))
