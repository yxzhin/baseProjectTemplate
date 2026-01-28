from collections.abc import AsyncGenerator

import discord.ext.test as dpytest
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.bot.app import create_bot
from src.bot.app.http import APIClient, HttpxTestsClient
from src.server.app.api import test_router, users_router
from src.server.app.db import Base, Database


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """Создает FastAPI приложение для тестирования."""
    app = FastAPI(prefix="/api")
    app.include_router(test_router)
    app.include_router(users_router)
    return app


@pytest.fixture(scope="session")
async def test_engine():
    """Создает асинхронный движок базы данных для тестов."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession]:
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


@pytest.fixture(scope="function")
async def httpx_client(app: FastAPI, db_session: AsyncSession):
    """Создает HTTP-клиент с переопределенной зависимостью базы данных для тестирования API."""

    async def override_get_db_session():
        yield db_session

    app.dependency_overrides[Database.dependency] = override_get_db_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def api_client_factory(httpx_client: AsyncClient):
    """Фабрика для создания HttpxTestsClient, обернутого в APIClient."""

    def _factory():
        return APIClient(http_client=HttpxTestsClient(httpx_client))

    return _factory


@pytest.fixture
def create_user(httpx_client):
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

        return response.json()

    return _create_user


@pytest.fixture
async def bot():
    """Создает и настраивает бота для тестирования с dpytest."""
    bot = create_bot()
    dpytest.configure(bot)  # pyright: ignore[reportGeneralTypeIssues]
    yield bot
    await dpytest.empty_queue()
