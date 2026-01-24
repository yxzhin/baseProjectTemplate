from os import listdir
from os.path import dirname, realpath
from sys import argv

from discord import Activity, ActivityType, Intents, Interaction, Status, app_commands
from discord.ext.commands import Bot

from ...shared import StructuredLogger
from .conf import Config
from .utils import Helpers


class TheBot(Bot):
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="IUseSlashCommandsLol",
            intents=intents,
            description=None,
            owner_id=Config.BOT_OWNER_ID,
            help_command=None,
        )

        self.tree.interaction_check = self.interaction_check
        self.tree.on_error = self.on_tree_error

    async def interaction_check(self, interaction: Interaction) -> bool:
        StructuredLogger.info(
            f"[bot] {interaction.user} issued command: {interaction.command.name} {interaction.command.extras} ({interaction.user.id}, {interaction.guild.id})"  # type: ignore
        )
        return True

    async def setup_hook(self):
        await self.load_all_cogs()
        await self.tree.sync()
        self.loop.create_task(self.set_presence())  # pyright: ignore[reportAttributeAccessIssue]

    async def set_presence(self):
        await self.wait_until_ready()
        await self.change_presence(
            status=Status.online,
            activity=Activity(
                type=ActivityType.listening,
                name=Config.BOT_STATUS_MESSAGE,
            ),
        )

    async def load_all_cogs(self, reload_: bool = False) -> list:
        failed = []
        abs_cogs_path = dirname(realpath(argv[0])) + "/cogs"

        for file in listdir(abs_cogs_path):
            if file[:-3] in Config.BOT_COGS:
                cog_path = Helpers.get_extension_path(abs_cogs_path, file)
                try:
                    if reload_:
                        await self.reload_extension(cog_path)
                        StructuredLogger.info(f"[bot] reloaded cog: {cog_path}")

                    else:
                        await self.load_extension(cog_path)
                        StructuredLogger.info(f"[bot] loaded cog: {cog_path}")

                except Exception as e:
                    failed.append(f"{cog_path}: {e}")
                    StructuredLogger.exception(
                        f"[bot] error while (re)loading cog: {cog_path}"
                    )

        return failed

    async def safe_reply(self, interaction: Interaction, content):
        if interaction.response.is_done():
            await interaction.followup.send(content)
        else:
            await interaction.response.send_message(content)

    async def on_tree_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original  # type: ignore

        if isinstance(error, app_commands.MissingPermissions):
            await self.safe_reply(
                interaction,
                f":x: permission denied: {', '.join(error.missing_permissions)}",  # pyright: ignore[reportAttributeAccessIssue]
            )
            return

        if isinstance(error, app_commands.BotMissingPermissions):
            await self.safe_reply(
                interaction,
                f":sob: not enough permissions for me: {', '.join(error.missing_permissions)}",  # pyright: ignore[reportAttributeAccessIssue]
            )
            return

        if isinstance(error, app_commands.CommandOnCooldown):
            await self.safe_reply(
                interaction,
                f":hourglass: too fast! retry after: `{error.retry_after:.1f}`s",  # pyright: ignore[reportAttributeAccessIssue]
            )
            return

        if isinstance(error, app_commands.TransformerError):
            await self.safe_reply(
                interaction,
                ":x: invalid user input",
            )
            return

        await self.safe_reply(
            interaction,
            f":x: an unknown error occurred: `{error}`",
        )

        raise error


__all__ = ["TheBot"]
