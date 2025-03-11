from datetime import date

from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepos
from src.repos.utils import rooms_ids_for_booking
from src.schemas.rooms import Room


class RoomsRepos(BaseRepos):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        result_query = rooms_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_all(RoomsOrm.id.in_(result_query))
