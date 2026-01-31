from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from ....shared import StructuredLogger
from ..db import Database
from .redis import RedisService


@asynccontextmanager
async def lifespan(_: Any) -> AsyncGenerator[None]:  # type: ignore
    """
    Контекстный менеджер для управления временем жизни приложения FastAPI.
    Инициализирует и закрывает ресурсы при старте и остановке приложения.
    """
    StructuredLogger.setup()
    try:
        await Database.init()
        await Database.test_connection()
        await RedisService.init()
        yield
    except Exception as e:
        StructuredLogger.exception("init.error", error=str(e))
        raise e
    finally:
        await Database.close()
        await RedisService.close()
