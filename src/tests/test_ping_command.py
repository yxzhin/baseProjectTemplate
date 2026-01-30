from src.bot.app.cogs import PingCog


async def test_ping_command(bot):
    """
    Тестирует команду /ping бота.
    Проверяет, что ответ начинается с 'pong' и содержит информацию о задержке.
    """
    response = await PingCog(bot).ping()
    assert response.startswith("`pong! latency: ~")
