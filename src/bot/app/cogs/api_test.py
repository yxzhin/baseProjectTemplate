from time import time

from discord import Interaction, app_commands
from discord.ext.commands import Cog

from .. import TheBot


class ApiTest(Cog):
    """
    Ког для тестирования взаимодействия с FastAPI приложением.
    Использует фабрику APIClient для создания Httpx или Aiohttp клиента.
    Позволяет измерить время отклика API.
    """

    def __init__(self, bot: TheBot):
        self.bot = bot

    async def api_test(self) -> str:
        """
        Тестирует эндпоинт /test/ FastAPI приложения.
        Измеряет время отклика API и возвращает результат вместе с задержкой.
        """
        start_time = time()
        async with self.bot.api_client_factory() as api_client:
            result = await api_client.get("/test/")
        end_time = time()
        api_latency = end_time - start_time
        return f"`{result}`\n`latency: ~{api_latency}s`"

    @app_commands.command(name="api_test", description="test the fastapi app")
    async def _api_test(self, interaction: Interaction):
        """Тестирует эндпоинт /test/ через команду /api_test."""
        await interaction.response.send_message(await self.api_test())


async def setup(bot: TheBot):
    await bot.add_cog(ApiTest(bot))
