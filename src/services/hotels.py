from datetime import date

from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.services.base import BaseDbService


class HotelService(BaseDbService):
    async def get_filtered_by_time(
        self,
        pagination: PaginationDep,
        title: str | None = None,
        location: str | None = None,
        *,
        date_from: date,
        date_to: date,
    ):
        hotels = await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            limit=pagination.per_page,
            offset=pagination.page,
            title=title,
            location=location,
        )
        return hotels

    async def get_hotel(self, hotel_id: int):
        hotel = await self.db.hotels.get_one(id=hotel_id)
        return hotel

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def put_hotel(self, hotel_data: HotelAdd, hotel_id: int) -> bool:
        hotel = await self.db.hotels.get_one_or_none(id=hotel_id)
        if hotel:
            await self.db.hotels.edit(hotel_data, id=hotel_id)
            await self.db.commit()
            return True
        return False

    async def patch_hotel(self, hotel_data: HotelPATCH, hotel_id: int) -> bool:
        hotel = await self.db.hotels.get_one_or_none(id=hotel_id)
        if hotel:
            await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
            await self.db.commit()
            return True
        return False

    async def delete_hotel(self, hotel_id: int) -> bool:
        hotel = await self.db.hotels.get_one_or_none(id=hotel_id)
        if hotel:
            await self.db.hotels.delete(id=hotel_id)
            await self.db.commit()
            return True
        return False
