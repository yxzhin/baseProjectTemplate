from ...shared import StructuredLogger
from . import create_bot
from .conf import Config


def main() -> None:
    """Точка входа для запуска бота. biscuits."""
    StructuredLogger.setup()
    bot = create_bot()
    bot.run(Config.BOT_TOKEN)


if __name__ == "__main__":
    main()
