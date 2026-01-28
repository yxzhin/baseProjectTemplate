import os

from ....shared import ConfigLoader

ConfigLoader.import_env()


class Config:
    """
    Конфигурационные параметры приложения, загружаемые из переменных окружения.
    Атрибуты доступны напрямую, без создания экземпляра класса.
    """

    BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
    BOT_SECRET = str(os.getenv("BOT_SECRET"))
    BOT_CLIENT_ID = int(os.getenv("BOT_CLIENT_ID"))  # type: ignore
    BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID"))  # type: ignore
    BOT_STATUS_MESSAGE = str(os.getenv("BOT_STATUS_MESSAGE"))
    BOT_COGS = str(os.getenv("BOT_COGS")).strip().split(",")

    API_URL = str(os.getenv("API_URL"))
