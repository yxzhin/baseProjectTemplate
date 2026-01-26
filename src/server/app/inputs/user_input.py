from pydantic import BaseModel


class UserAddInput(BaseModel):
    discord_id: int
    username: str
    avatar_url: str | None
