from datetime import date
from random import randint

from src.schemas.bookings import BookingsAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    ## create
    booking_data = BookingsAdd(
        room_id=room_id,
        date_from=date(2025, 12, 30),
        date_to=date(2026, 1, 10),
        user_id=user_id,
        price=randint(100, 1000),
    )
    await db.bookings.add(booking_data)

    ## read
    new_booking = (await db.bookings.get_all())[0]
    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    ## update
    await db.bookings.edit(
        data=BookingsAdd(
            room_id=room_id,
            date_from=date(2026, 1, 10),
            date_to=date(2026, 1, 20),
            user_id=user_id,
            price=99,
        ),
        exclude_unset=True,
        user_id=new_booking.user_id,
        room_id=new_booking.room_id,
    )
    booking_data = (await db.bookings.get_all())[0]
    assert booking_data.date_from == date(2026, 1, 10)
    assert booking_data.date_to == date(2026, 1, 20)
    assert booking_data.price == 99

    ## delete
    await db.bookings.delete(user_id=new_booking.user_id, room_id=new_booking.room_id)
    assert await db.bookings.get_all() == []
