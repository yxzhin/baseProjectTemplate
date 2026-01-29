from fastapi import APIRouter, HTTPException, Response, status

from ...inputs import UserCreateInput
from ...services import UserService
from ..responses import UserOutResponse, UsersOutResponse

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/{discord_id}", response_model=UserOutResponse)
async def get_user_by_discord_id(discord_id: int, user_service: UserService):
    """Получает пользователя по его Discord ID."""
    user = await user_service.get_user_by_discord_id(discord_id=discord_id)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user


@users_router.get("/username/{username}", response_model=UserOutResponse)
async def get_user_by_username(username: str, user_service: UserService):
    """Получает пользователя по его имени пользователя."""
    user = await user_service.get_user_by_username(username=username)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user


@users_router.get("/", response_model=UsersOutResponse)
async def get_users(
    user_service: UserService,
    page: int | None = None,
    limit: int | None = None,
):
    """Получает список пользователей с поддержкой пагинации."""
    if page is not None and page < 1 or limit is not None and limit < 1:
        raise HTTPException(
            status_code=400, detail="page and limit must be greater than 0"
        )

    if page is None:
        page = 1
    if limit is None:
        limit = 10

    users = await user_service.get_users(page=page, limit=limit)
    return {"users": users, "total": len(users)}


@users_router.post("/add", response_model=UserOutResponse)
async def add_user(
    user: UserCreateInput,
    response: Response,
    user_service: UserService,
):
    """Добавляет нового пользователя в базу данных."""
    if await user_service.get_user_by_discord_id(discord_id=user.discord_id):
        raise HTTPException(status_code=400, detail="discord id already taken")

    if await user_service.get_user_by_username(username=user.username):
        raise HTTPException(status_code=400, detail="username already taken")

    new_user = await user_service.create_user(user=user)
    response.status_code = status.HTTP_201_CREATED
    return new_user
