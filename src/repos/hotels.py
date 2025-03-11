from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepos
from src.repos.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepos(BaseRepos):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        limit: int,
        offset: int,
        title: str | None = None,
        location: str | None = None,
    ):
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
                lambda x: self.schema.model_validate(x, from_attributes=True),
                result.all(),
            )
        )
