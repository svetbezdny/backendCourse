from datetime import date

from sqlalchemy import select

from src.exceptions import AllRoomsAreBookedException
from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepos
from src.repos.mappers.mappers import BookingsDataMapper
from src.repos.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingsRequest


class BookingsRepos(BaseRepos):
    model = BookingsOrm
    mapper = BookingsDataMapper

    async def get_bookings_with_today_checkin(self) -> list:
        query = select(self.model).filter(self.model.date_from == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(b) for b in result.scalars().all()]

    async def add_booking(self, data: BookingsRequest, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book = rooms_ids_to_book_res.scalars().all()
        if data.room_id in rooms_ids_to_book:
            return await self.add(data)
        raise AllRoomsAreBookedException
