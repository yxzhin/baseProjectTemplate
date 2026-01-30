from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ...db import Base


class User(Base):
    """
    Модель пользователя.
    Представляет пользователя с его Discord ID, именем пользователя и URL аватара.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    discord_id: Mapped[int] = mapped_column(
        BigInteger(), nullable=False, unique=True, index=True
    )
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    balance: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    rank: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    inventory: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, discord_id={self.discord_id})>"
