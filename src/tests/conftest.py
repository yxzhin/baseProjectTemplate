from collections.abc import AsyncGenerator, Callable
from typing import Any

import discord.ext.test as dpytest
import pytest
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.bot.app import TheBot, create_bot
from src.bot.app.http import APIClient, HttpxTestsClient
from src.server.app.api.routers import *
from src.server.app.db import Base
from src.server.app.di import RepositoryProvider, ServiceProvider, TestDatabaseProvider


@pytest.fixture
async def test_engine() -> AsyncGenerator[AsyncEngine, Any]:
    """Создает асинхронный движок базы данных для тестов."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, Any]:
    """Создает новую сессию и откатывает все изменения после теста."""
    async with test_engine.connect() as conn:
        transaction = await conn.begin()

        sessionmaker = async_sessionmaker(
            bind=conn,
            expire_on_commit=False,
            class_=AsyncSession,
        )

        async with sessionmaker() as session:
            await session.begin_nested()

            @event.listens_for(session.sync_session, "after_transaction_end")
            def restart_savepoint(sess, trans):
                if trans.nested and not trans._parent.nested:
                    sess.begin_nested()

            yield session

        await transaction.rollback()


@pytest.fixture
async def app_container(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncContainer, Any]:
    app_container = make_async_container(
        TestDatabaseProvider(session=db_session),
        RepositoryProvider(),
        ServiceProvider(),
    )
    yield app_container
    await app_container.close()


@pytest.fixture
async def bot_container(api_client_factory) -> AsyncGenerator[AsyncContainer, Any]:
    from src.bot.app.di import create_bot_container

    container = create_bot_container(api_client_factory=api_client_factory)

    yield container
    await container.close()


@pytest.fixture
def app(app_container: AsyncContainer) -> FastAPI:
    """Создает FastAPI приложение для тестирования."""
    app = FastAPI()
    app.include_router(test_router)
    app.include_router(users_router)
    app.include_router(database_router)

    setup_dishka(container=app_container, app=app)
    return app


@pytest.fixture
async def httpx_client(app: FastAPI) -> AsyncGenerator[AsyncClient, Any]:
    """Создает HTTP-клиент для тестирования API."""

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture
def api_client_factory(httpx_client: AsyncClient) -> Callable[[], APIClient]:
    """Фабрика для создания HttpxTestsClient, обернутого в APIClient."""

    def _factory():
        return APIClient(http_client=HttpxTestsClient(httpx_client))

    return _factory


@pytest.fixture
def create_user(httpx_client: AsyncClient) -> Callable[[int, str, str | None], Any]:
    """
    Фикстура для создания пользователя через API.
    Возвращает функцию, которая создает пользователя с заданными параметрами.
    """

    async def _create_user(
        discord_id: int,
        username: str,
        avatar_url: str | None = None,
    ) -> dict:
        payload = {
            "discord_id": discord_id,
            "username": username,
            "avatar_url": avatar_url or "http://placehold.co/730x370",
        }

        response = await httpx_client.post("/users/add", json=payload)
        assert response.status_code == 201, response.text

        json = response.json()
        assert json["success"] is True

        return json["user"]

    return _create_user


@pytest.fixture
async def bot(api_client_factory) -> AsyncGenerator[TheBot, Any]:
    """Создает и настраивает бота для тестирования с dpytest."""
    bot = create_bot(api_client_factory=api_client_factory)
    dpytest.configure(bot)  # pyright: ignore[reportGeneralTypeIssues]
    yield bot
    await dpytest.empty_queue()
