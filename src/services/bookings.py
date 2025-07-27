from src.api.dependencies import UserIdDep
from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException
from src.schemas.bookings import BookingsAdd, BookingsRequest
from src.services.base import BaseDbService


class BookingService(BaseDbService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_all(user_id=user_id)

    async def create_booking(self, user_id: UserIdDep, bookings_data: BookingsRequest):
        try:
            await self.db.users.get_one(id=user_id)
        except ObjectNotFoundException:
            raise ObjectNotFoundException(detail=f"No user with id {user_id}")
        try:
            room = await self.db.rooms.get_one(id=bookings_data.room_id)
        except ObjectNotFoundException:
            raise ObjectNotFoundException(
                detail=f"No room with id {bookings_data.room_id}"
            )
        hotel = await self.db.hotels.get_one_or_none(id=room.hotel_id)
        bookings_data_ = BookingsAdd(
            user_id=user_id, price=room.price, **bookings_data.model_dump()
        )
        try:
            booking = await self.db.bookings.add_booking(bookings_data_, hotel.id)  # type: ignore
        except AllRoomsAreBookedException:
            raise AllRoomsAreBookedException
        await self.db.commit()
        return booking
