from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...services import UserService
from ...utils import Seeder
from ..responses import GeneralMessageResponse

database_router = APIRouter(
    prefix="/database",
    tags=["database"],
    route_class=DishkaRoute,
)


@database_router.get("/seed", response_model=GeneralMessageResponse)
@inject
async def seed_database(
    user_service: FromDishka[UserService],
    session: FromDishka[AsyncSession],
):
    """Заполняет базу данных начальными данными с помощью Seeder."""
    if not await Seeder.seed(user_service=user_service, session=session):
        raise HTTPException(status_code=500, detail="failed to seed the database")
    return {"message": "database seeded successfully!! :tada:"}


@database_router.get("/clear", response_model=GeneralMessageResponse)
@inject
async def clear_database(
    session: FromDishka[AsyncSession],
):
    """Очищает начальные данные в базе данных с помощью Seeder."""
    await Seeder.clear(session=session)
    return {"message": "database cleared successfully!! :tada:"}
