import orjson
import pytest
from httpx import ASGITransport, AsyncClient

from src.config import settings
from src.database import Base, async_session_maker_null_pool, engine_null_pool
from src.main import app
from src.models import *  # noqa: F403
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "test"


@pytest.fixture(scope="session", autouse=True)
async def database_init(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with (
        open("tests/mock_hotels.json", "r", encoding="utf-8") as mh,
        open("tests/mock_rooms.json", "r", encoding="utf-8") as mr,
    ):
        hotels_data = orjson.loads(mh.read())
        rooms_data = orjson.loads(mr.read())

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        for hotel in hotels_data:
            await db.hotels.add(HotelAdd(**hotel))
            await db.commit()

        for room in rooms_data:
            await db.rooms.add(RoomAdd(**room))
            await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(database_init):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
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
