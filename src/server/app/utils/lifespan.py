from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from ....shared import StructuredLogger
from ..db import Database
from ..services import RedisService


@asynccontextmanager
async def lifespan(_: Any) -> AsyncGenerator[None]:  # type: ignore
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
