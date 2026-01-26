from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.server.app.api import test_router, users_router
from src.server.app.db import Base, Database


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(test_router)
    app.include_router(users_router)
    return app


@pytest.fixture(scope="session")
async def test_engine():
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
async def client(app: FastAPI, db_session: AsyncSession):
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
def create_user(client):
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

        response = await client.post("/users/add", json=payload)
        assert response.status_code == 201, response.text

        return response.json()

    return _create_user
