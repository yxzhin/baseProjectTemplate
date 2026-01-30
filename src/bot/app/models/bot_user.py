from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator


class BotUser(BaseModel):
    id: int
    discord_id: int
    username: str
    avatar_url: str | None
    balance: int
    rank: int
    inventory: list[int] | None
    created_at: datetime
    updated_at: datetime

    @field_validator("inventory", mode="before")
    @classmethod
    def split_inventory(cls, value: Any) -> Any:
        if value is not None and not isinstance(value, list):
            return map(int, str(value).split(","))
        return value
