from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import UserIdDep, async_db_conn
from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException
from src.schemas.bookings import BookingsRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("", response_model=list[BookingsRequest])
async def get_all_bookings(db: async_db_conn):
    all_bookings = await BookingService(db).get_all_bookings()
    if not all_bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bookings")
    return all_bookings


@router.get("/me", response_model=list[BookingsRequest])
async def get_my_bookings(db: async_db_conn, user_id: UserIdDep):
    my_bookings = await BookingService(db).get_my_bookings(user_id)
    if not my_bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bookings")
    return my_bookings


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(
    db: async_db_conn, user_id: UserIdDep, bookings_data: BookingsRequest
):
    try:
        booking = await BookingService(db).create_booking(user_id, bookings_data)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex.detail,
        )
    except AllRoomsAreBookedException as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ex.detail,
        )
    return {
        "message": "Successful",
        "data": booking,
    }
