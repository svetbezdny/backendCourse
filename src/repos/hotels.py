from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import HotelDoesNotExistException, MismatchedDatesException
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepos
from src.repos.mappers.mappers import HotelDataMapper
from src.repos.utils import rooms_ids_for_booking


class HotelsRepos(BaseRepos):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        limit: int,
        offset: int,
        title: str | None = None,
        location: str | None = None,
    ) -> list:
        if date_from >= date_to:
            raise MismatchedDatesException

        rooms_ids = rooms_ids_for_booking(date_from, date_to)
        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids))
        )

        hotels_query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids))
        if title is not None:
            hotels_query = hotels_query.where(self.model.title.ilike(f"%{title}%"))
        if location is not None:
            hotels_query = hotels_query.where(
                self.model.location.ilike(f"%{location}%")
            )
        result = await self.session.scalars(
            hotels_query.limit(limit).offset(limit * (offset - 1))
        )
        return list(
            map(
                lambda x: self.mapper.map_to_domain_entity(x),
                result.all(),
            )
        )

    async def get_one(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        try:
            res = result.scalar_one()
            return self.mapper.map_to_domain_entity(res)
        except NoResultFound:
            raise HotelDoesNotExistException
