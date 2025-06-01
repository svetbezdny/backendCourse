from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepos
from src.repos.mappers.mappers import RoomsDataMapper
from src.repos.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomWithRels


class RoomsRepos(BaseRepos):
    model = RoomsOrm
    mapper = RoomsDataMapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(m) for m in result.unique().scalars().all()]

    async def get_one_or_none(self, **kwargs):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**kwargs)
        )
        result = await self.session.execute(query)
        res = result.scalar_one_or_none()
        return RoomWithRels.model_validate(res)
