from src.bot.app.cogs import Reload


async def test_reload_command(bot):
    """
    Тестирует команду /reload бота.
    Проверяет успешную перезагрузку кога 'ping'.
    """
    await bot.load_extension("src.bot.app.cogs.ping")
    response = await Reload(bot, abs_cogs_path="src/bot/app/cogs").reload("ping")
    assert response[1] is True
    await bot.unload_extension("src.bot.app.cogs.ping")


async def test_reload_all_command(bot):
    """
    Тестирует команду /reload_all бота.
    Проверяет успешную перезагрузку всех когов.
    """
    failed_to_load = await bot.load_all_cogs(
        abs_cogs_path="src/bot/app/cogs", log=False
    )
    assert len(failed_to_load) == 0

    response = await Reload(bot, abs_cogs_path="src/bot/app/cogs").reload_all()
    assert len(response) == 0

    failed_to_unload = await bot.unload_all_cogs(
        abs_cogs_path="src/bot/app/cogs", log=False
    )
    assert len(failed_to_unload) == 0
