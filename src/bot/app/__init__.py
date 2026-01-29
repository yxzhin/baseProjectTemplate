from os import listdir
from os.path import dirname, realpath
from sys import argv

from discord import Activity, ActivityType, Intents, Interaction, Status, app_commands
from discord.ext.commands import Bot

from ...shared import StructuredLogger
from .conf import Config
from .http import APIClient
from .utils import Helpers


class TheBot(Bot):
    """
    Основной класс бота, наследующий от discord.ext.commands.Bot.
    Настраивает префикс команд, интенты, обработку ошибок и загрузку когов.
    """

    def __init__(self, api_client_factory=APIClient):
        intents = Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="IUseSlashCommandsLol",
            intents=intents,
            description=None,
            owner_id=Config.BOT_OWNER_ID,
            help_command=None,
        )

        self.api_client_factory = api_client_factory

        self.tree.interaction_check = self._interaction_check
        self.tree.on_error = self._on_tree_error

    async def setup_hook(self):
        """
        Загружает все указанные в конфиге когы и синхронизирует дерево команд.
        """
        await self.load_all_cogs()
        await self.tree.sync()
        self.loop.create_task(self._set_presence())  # type: ignore

    async def load_all_cogs(
        self, reload_: bool = False, abs_cogs_path: str | None = None, log: bool = True
    ) -> list:
        """
        Загружает или перезагружает все когы, указанные в конфиге.
        Возвращает список неудачных загрузок.
        """
        failed = []
        abs_cogs_path = (
            abs_cogs_path if abs_cogs_path else dirname(realpath(argv[0])) + "/cogs"
        )

        for file in listdir(abs_cogs_path):
            if file[:-3] in Config.BOT_COGS:
                cog_path = Helpers.get_extension_path(abs_cogs_path, file)
                try:
                    if reload_:
                        await self.reload_extension(cog_path)
                        if log:
                            StructuredLogger.info(f"[bot] reloaded cog: {cog_path}")

                    else:
                        await self.load_extension(cog_path)
                        if log:
                            StructuredLogger.info(f"[bot] loaded cog: {cog_path}")

                except Exception as e:
                    failed.append(f"{cog_path}: {e}")
                    if log:
                        StructuredLogger.exception(
                            f"[bot] error while (re)loading cog: {cog_path}"
                        )

        return failed

    async def unload_all_cogs(
        self, abs_cogs_path: str | None = None, log: bool = True
    ) -> list:
        """
        Выгружает все когы, указанные в конфиге.
        Возвращает список неудачных выгрузок.
        """
        failed = []
        abs_cogs_path = (
            abs_cogs_path if abs_cogs_path else dirname(realpath(argv[0])) + "/cogs"
        )

        for file in listdir(abs_cogs_path):
            if file[:-3] in Config.BOT_COGS:
                cog_path = Helpers.get_extension_path(abs_cogs_path, file)
                try:
                    await self.unload_extension(cog_path)
                    if log:
                        StructuredLogger.info(f"[bot] unloaded cog: {cog_path}")

                except Exception as e:
                    failed.append(f"{cog_path}: {e}")
                    if log:
                        StructuredLogger.exception(
                            f"[bot] error while unloading cog: {cog_path}"
                        )

        return failed

    async def _interaction_check(self, interaction: Interaction) -> bool:
        """
        Логирует каждое взаимодействие с ботом.
        """
        StructuredLogger.info(
            "[bot] issued command",
            user=str(interaction.user),  # type: ignore
            command_name=interaction.command.name,  # type: ignore
            command_extras=interaction.command.extras,  # type: ignore
            user_id=interaction.user.id,  # type: ignore
            guild_id=interaction.guild.id,  # type: ignore
        )
        return True

    async def _set_presence(self):
        """
        Устанавливает статус бота после его готовности.
        """
        await self.wait_until_ready()
        await self.change_presence(
            status=Status.online,
            activity=Activity(
                type=ActivityType.listening,
                name=Config.BOT_STATUS_MESSAGE,
            ),
        )

    async def _safe_reply(self, interaction: Interaction, content):
        """
        Безопасно отвечает на взаимодействие, учитывая его состояние.
        """
        if interaction.response.is_done():
            await interaction.followup.send(content)
        else:
            await interaction.response.send_message(content)

    async def _on_tree_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        """
        Универсальная обработка ошибок для всех команд бота.
        Отправляет пользователю понятные сообщения об ошибках.
        """
        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original  # type: ignore

        if isinstance(error, app_commands.MissingPermissions):
            await self._safe_reply(
                interaction,
                f":x: permission denied: {', '.join(error.missing_permissions)}",  # pyright: ignore[reportAttributeAccessIssue]
            )
            return

        if isinstance(error, app_commands.BotMissingPermissions):
            await self._safe_reply(
                interaction,
                f":sob: not enough permissions for me: {', '.join(error.missing_permissions)}",  # pyright: ignore[reportAttributeAccessIssue]
            )
            return

        if isinstance(error, app_commands.CommandOnCooldown):
            await self._safe_reply(
                interaction,
                f":hourglass: too fast! retry after: `{error.retry_after:.1f}`s",  # pyright: ignore[reportAttributeAccessIssue]
            )
            return

        if isinstance(error, app_commands.TransformerError):
            await self._safe_reply(
                interaction,
                ":x: invalid user input",
            )
            return

        await self._safe_reply(
            interaction,
            f":x: an unknown error occurred: `{error}`",
        )

        raise error

    async def close(self):
        """
        Закрывает соединение бота и выполняет необходимые операции очистки.
        """
        await super().close()
        StructuredLogger.info("[bot] closed")


def create_bot(api_client_factory=APIClient) -> TheBot:
    """
    Создает и настраивает экземпляр бота TheBot.
    Возвращает готовый к использованию экземпляр бота.
    """
    bot = TheBot(api_client_factory=api_client_factory)

    @bot.event
    async def on_ready():
        StructuredLogger.info(f"[bot] started as {bot.user}")

    return bot


__all__ = ["TheBot"]
