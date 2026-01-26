from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserOutResponse(BaseModel):
    id: int
    discord_id: int
    username: str
    avatar_url: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UsersOutResponse(BaseModel):
    users: list[UserOutResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)
