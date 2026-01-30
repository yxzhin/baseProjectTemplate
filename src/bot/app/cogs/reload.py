from os.path import dirname, realpath
from sys import argv

from discord import Interaction
from discord.app_commands import command, describe
from discord.ext.commands import Cog, is_owner

from ....shared import StructuredLogger
from .. import TheBot
from ..utils import Helpers


class ReloadCog(Cog):
    def __init__(self, bot: TheBot, abs_cogs_path: str | None = None):
        self.bot = bot
        self.abs_cogs_path = (
            abs_cogs_path if abs_cogs_path else dirname(realpath(argv[0])) + "/cogs"
        )

    async def reload(self, cog: str) -> tuple[str, bool]:
        """
        Перезагружает указанный ког бота.
        Использует Helpers.get_extension_path для получения пути расширения.
        Возвращает кортеж с сообщением и статусом успеха.
        """
        try:
            file = f"{cog}.py"
            cog_path = Helpers.get_extension_path(self.abs_cogs_path, file)
            await self.bot.reload_extension(cog_path)
            return f":white_check_mark: cog `{cog}` reloaded successfully", True
        except Exception as e:
            return f":x: an error occurred:\n```{e}```", False

    async def reload_all(self) -> list:
        """
        Перезагружает все когы бота, указанные в конфиге.
        Использует метод TheBot.load_all_cogs для перезагрузки.
        Возвращает список неудачных загрузок.
        """
        failed = await self.bot.load_all_cogs(
            reload_=True, abs_cogs_path=self.abs_cogs_path
        )
        return failed

    @command(name="reload", description="reload a cog")
    @describe(cog="target cog filename (ex. ping)")
    @is_owner()
    async def _reload(self, interaction: Interaction, cog: str):
        """Перезагружает указанный ког бота через команду /reload."""
        result = await self.reload(cog)
        await self.bot.tree.sync(guild=interaction.guild)

        if result[1]:
            await interaction.response.send_message(result[0])
            StructuredLogger.info(f"[bot] successfully reloaded cog: {cog}")
            return

        StructuredLogger.exception(f"[bot] error while reloading cog: {cog}")
        await interaction.response.send_message(result[0])

    @command(name="reload_all", description="reload all cogs")
    @is_owner()
    async def _reload_all(self, interaction: Interaction):
        """Перезагружает все когы бота через команду /reload_all."""
        failed = await self.reload_all()
        await self.bot.tree.sync(guild=interaction.guild)

        if len(failed) > 0:
            await interaction.response.send_message(
                ":x: some errors occurred:\n" + "\n".join(failed),
            )
            return

        await interaction.response.send_message(
            ":white_check_mark: all cogs reloaded successfully"
        )


async def setup(bot: TheBot):
    await bot.add_cog(ReloadCog(bot))
