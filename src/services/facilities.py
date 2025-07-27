from src.exceptions import ObjectNotFoundException
from src.schemas.facilities import Facility
from src.services.base import BaseDbService


class FacilityService(BaseDbService):
    async def get_facilities(self):
        facilities_db = await self.db.facilities.get_all()
        if not facilities_db:
            raise ObjectNotFoundException
        return facilities_db

    async def create_facility(self, facility_data: Facility):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()
        return facility
