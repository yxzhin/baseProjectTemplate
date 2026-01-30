from datetime import datetime

from pydantic import BaseModel, ConfigDict

from . import BaseResponse


class UserOutModel(BaseModel):
    """Модель выходных данных для представления пользователя."""

    id: int
    discord_id: int
    username: str
    avatar_url: str | None
    balance: int
    rank: int
    inventory: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserOutResponse(BaseResponse):
    user: UserOutModel | None

    model_config = ConfigDict(from_attributes=True)


class UsersOutResponse(BaseResponse):
    """Модель выходных данных для представления списка пользователей."""

    users: list[UserOutModel]
    total: int

    model_config = ConfigDict(from_attributes=True)
