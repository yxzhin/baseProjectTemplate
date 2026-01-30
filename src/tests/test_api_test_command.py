from src.bot.app.cogs import ApiTestCog


async def test_api_test_command(bot):
    """
    Тестирует команду /api_test бота.
    Проверяет, что ответ содержит сообщение об успешном тестировании API.
    """
    response = await ApiTestCog(bot).api_test()
    assert "it works!! :tada:" in response
