from pydantic import BaseModel


class UserCreateInput(BaseModel):
    """Модель входных данных для добавления пользователя."""

    discord_id: int
    username: str
    avatar_url: str | None
