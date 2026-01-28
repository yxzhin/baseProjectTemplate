from src.bot.app.cogs import Ping


async def test_ping_command(bot):
    """
    Тестирует команду /ping бота.
    Проверяет, что ответ начинается с 'pong' и содержит информацию о задержке.
    """
    response = await Ping(bot).ping()
    assert response.startswith("`pong! latency: ~")
