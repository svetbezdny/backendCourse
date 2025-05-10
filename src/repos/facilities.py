from sqlalchemy import delete, insert, select

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repos.base import BaseRepos
from src.repos.mappers.mappers import FacilitiesDataMapper
from src.schemas.facilities import RoomFacility


class FacilitiesRepos(BaseRepos):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepos(BaseRepos):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def set_room_facilities(
        self, room_id: int, facilities_ids: list[int]
    ) -> None:
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(query)
        cur_facilities_ids = res.scalars().all()

        del_ids = list(set(cur_facilities_ids) - set(facilities_ids))
        add_ids = list(set(facilities_ids) - set(cur_facilities_ids))

        if del_ids:
            stmt = delete(self.model).filter(
                self.model.room_id == room_id, self.model.facility_id.in_(del_ids)
            )
            await self.session.execute(stmt)

        if add_ids:
            stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in add_ids]
            )
            await self.session.execute(stmt)
