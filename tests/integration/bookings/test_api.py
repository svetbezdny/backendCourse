import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-07-15", "2025-08-20", 201),
        (1, "2025-07-15", "2025-08-20", 201),
        (1, "2025-07-15", "2025-08-20", 201),
        (1, "2025-07-16", "2025-08-21", 201),
        (1, "2025-07-15", "2025-08-20", 201),
        (1, "2025-07-15", "2025-08-21", 500),
        (1, "2025-07-22", "2025-08-28", 500),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, authenticated_ac):
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == status_code
    if status_code == 201:
        res = response.json()
        assert isinstance(res, dict)
        assert res["transaction"] == "Successful"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_booking():
    async for db in get_db_null_pool():
        await db.bookings.delete()
        await db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_quantity",
    [
        (1, "2025-07-15", "2025-08-20", 1),
        (1, "2025-07-16", "2025-08-21", 2),
        (1, "2025-07-17", "2025-08-22", 3),
    ],
)
async def test_add_and_get_bookings(
    delete_all_booking, room_id, date_from, date_to, booked_quantity, authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == 201

    get_my_bookings_response = await authenticated_ac.get("/bookings/me")
    assert get_my_bookings_response.status_code == 200
    assert len(get_my_bookings_response.json()) == booked_quantity
