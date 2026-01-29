from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserOutResponse(BaseModel):
    """Модель выходных данных для представления пользователя."""

    id: int
    discord_id: int
    username: str
    avatar_url: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UsersOutResponse(BaseModel):
    """Модель выходных данных для представления списка пользователей."""

    users: list[UserOutResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)
