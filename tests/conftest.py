from typing import AsyncGenerator
from unittest import mock

import orjson
import pytest
from httpx import ASGITransport, AsyncClient

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from src.api.dependencies import get_db  # noqa: E402
from src.config import settings  # noqa: E402
from src.database import async_session_maker_null_pool  # noqa: E402
from src.database import Base, engine_null_pool  # noqa: E402
from src.main import app  # noqa: E402
from src.models import *  # noqa: F403,  E402
from src.schemas.hotels import HotelAdd  # noqa: E402
from src.schemas.rooms import RoomAdd  # noqa: E402
from src.utils.db_manager import DBManager  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "test"


async def get_db_null_pool() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture()
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def database_init():
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with (
        open("tests/mock_hotels.json", "r", encoding="utf-8") as mh,
        open("tests/mock_rooms.json", "r", encoding="utf-8") as mr,
    ):
        hotels_data = orjson.loads(mh.read())
        rooms_data = orjson.loads(mr.read())

    async with DBManager(session_factory=async_session_maker_null_pool) as conn:
        for hotel in hotels_data:
            await conn.hotels.add(HotelAdd(**hotel))
            await conn.commit()

        for room in rooms_data:
            await conn.rooms.add(RoomAdd(**room))
            await conn.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, database_init):
    response = await ac.post(
        "/auth/register",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "age": "30",
            "city": "New York",
            "email": "test@test.com",
            "password": "qwerty1234",
        },
    )
    assert response.status_code == 201


@pytest.fixture(scope="session")
async def authenticated_ac(ac, register_user):
    response = await ac.post(
        "/auth/login", json={"email": "test@test.com", "password": "qwerty1234"}
    )
    assert response.status_code == 200
    assert "access_token" in response.cookies
    yield ac
