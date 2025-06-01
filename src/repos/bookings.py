from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepos
from src.repos.mappers.mappers import BookingsDataMapper


class BookingsRepos(BaseRepos):
    model = BookingsOrm
    mapper = BookingsDataMapper

    async def get_bookings_with_today_checkin(self) -> list:
        query = select(self.model).filter(self.model.date_from == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(b) for b in result.scalars().all()]
