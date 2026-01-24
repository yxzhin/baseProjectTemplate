from ...shared import StructuredLogger
from . import TheBot
from .conf import Config


def main() -> None:
    StructuredLogger.setup()
    bot = TheBot()

    @bot.event
    async def on_ready():
        StructuredLogger.info(f"[bot] started as {bot.user}")

    bot.run(str(Config.BOT_TOKEN))


if __name__ == "__main__":
    main()
