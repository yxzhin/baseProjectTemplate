from pydantic import BaseModel


class UserAddInput(BaseModel):
    """Модель входных данных для добавления пользователя."""

    discord_id: int
    username: str
    avatar_url: str | None
