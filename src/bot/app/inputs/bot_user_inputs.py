from pydantic import BaseModel


class BotUserCreateInput(BaseModel):
    discord_id: int
    username: str
    avatar_url: str | None = None
