from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import async_db_conn
from src.schemas.bookings import BookingsAdd, BookingsRequest

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_booking(
    db: async_db_conn, user_id: int, bookings_data: BookingsRequest
):
    user = await db.users.get_one_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No user with id {user_id}",
        )
    room = await db.rooms.get_one_or_none(id=bookings_data.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No room with id {bookings_data.room_id}",
        )
    bookings_data_ = BookingsAdd(
        user_id=user_id, price=room.price, **bookings_data.model_dump()
    )
    booking = await db.bookings.add(bookings_data_)
    await db.commit()
    return {
        "transaction": "Successful",
        "data": booking,
    }
