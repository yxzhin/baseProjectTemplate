from typing import Any

from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject
from fastapi import APIRouter
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import User
from ..responses import TestResponse

test_router = APIRouter(
    prefix="/test",
    tags=["test"],
    route_class=DishkaRoute,
)


@test_router.get("/", response_model=TestResponse)
@inject
async def test(
    session: FromDishka[AsyncSession],
) -> Any:  # type: ignore
    """
    Проверочный эндпоинт для тестирования работоспособности API.
    Возвращает сообщение и количество пользователей в базе данных.
    """
    query = select(func.count()).select_from(User)
    users_count = await session.scalar(query)
    return {
        "success": True,
        "message": "it works!! :tada:",
        "users_count": users_count,
    }
