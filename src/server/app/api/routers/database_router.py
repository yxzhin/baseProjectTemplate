from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import Database
from ...utils import Seeder

database_router = APIRouter(prefix="/database", tags=["database"])


@database_router.get("/seed")
async def seed_database(
    session: AsyncSession = Depends(Database.dependency),
):
    if not await Seeder.seed(session=session):
        raise HTTPException(status_code=500, detail="failed to seed the database")
    return {"message": "database seeded successfully!! :tada:"}


@database_router.get("/clear")
async def clear_database(
    session: AsyncSession = Depends(Database.dependency),
):
    await Seeder.clear(session=session)
    return {"message": "database cleared successfully!! :tada:"}
