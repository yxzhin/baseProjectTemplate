from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import Database
from ...inputs import UserAddInput
from ...repositories import UserRepository
from ..responses import UserOutResponse, UsersOutResponse

users_router = APIRouter(prefix="/users")


@users_router.get("/{discord_id}", response_model=UserOutResponse)
async def get_user_by_discord_id(
    discord_id: int,
    session: AsyncSession = Depends(Database.dependency),
):
    user = await UserRepository.get_user_by_discord_id(
        session=session, discord_id=discord_id
    )

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user


@users_router.get("/username/{username}", response_model=UserOutResponse)
async def get_user_by_username(
    username: str,
    session: AsyncSession = Depends(Database.dependency),
):
    user = await UserRepository.get_user_by_username(session=session, username=username)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user


@users_router.get("", response_model=UserOutResponse | UsersOutResponse)
async def get_users(
    page: int | None = None,
    limit: int | None = None,
    session: AsyncSession = Depends(Database.dependency),
):
    if page is not None and page < 1 or limit is not None and limit < 1:
        raise HTTPException(
            status_code=400, detail="page and limit must be greater than 0"
        )

    if page is None:
        page = 1
    if limit is None:
        limit = 10

    offset = (page - 1) * limit
    result = await session.execute(
        UserRepository.get_users_query().offset(offset).limit(limit)
    )
    users = result.scalars().all()
    return {"users": users, "total": len(users)}


@users_router.post("/add", response_model=UserOutResponse)
async def add_user(
    user: UserAddInput,
    response: Response,
    session: AsyncSession = Depends(Database.dependency),
):
    if await UserRepository.get_user_by_discord_id(
        session=session, discord_id=user.discord_id
    ):
        raise HTTPException(status_code=400, detail="discord id already taken")

    if await UserRepository.get_user_by_username(
        session=session, username=user.username
    ):
        raise HTTPException(status_code=400, detail="username already taken")

    new_users = await UserRepository.add_users(session=session, users=[user])
    response.status_code = status.HTTP_201_CREATED
    return new_users[0]
