from src.bot.app.cogs import ApiTest


async def test_api_test_command(bot):
    """
    Тестирует команду /api_test бота.
    Проверяет, что ответ содержит сообщение об успешном тестировании API.
    """
    response = await ApiTest(bot).api_test()
    assert "it works!! :tada:" in response
