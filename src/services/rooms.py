from datetime import date

from src.exceptions import (HotelDoesNotExistException,
                            RoomDoesNotExistException)
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import (RoomAdd, RoomAddRequest, RoomPatch,
                               RoomPatchRequest)
from src.services.base import BaseDbService


class RoomService(BaseDbService):
    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms = await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        return rooms

    async def get_room(self, hotel_id: int, room_id: int):
        room = await self.db.rooms.get_one(hotel_id=hotel_id, id=room_id)
        return room

    async def create_room(self, hotel_id: int, room_data: RoomAddRequest):
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        try:
            await self.db.hotels.get_one(id=_room_data.hotel_id)
        except HotelDoesNotExistException:
            raise

        room = await self.db.rooms.add(_room_data)

        rooms_fac_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id)  # type: ignore
            for f_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_fac_data)
        await self.db.commit()
        return room

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        try:
            await self.db.rooms.edit(_room_data, id=room_id)
        except RoomDoesNotExistException:
            raise

        await self.db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=room_data.facilities_ids
        )
        await self.db.commit()

    async def partial_edit_room(
        self, hotel_id: int, room_id: int, room_data: RoomPatchRequest
    ):
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        try:
            await self.db.rooms.get_one(hotel_id=hotel_id, id=room_id)
        except RoomDoesNotExistException:
            raise
        await self.db.rooms.edit(
            _room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id
        )
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        try:
            await self.db.rooms.get_one(hotel_id=hotel_id, id=room_id)
        except RoomDoesNotExistException:
            raise
        await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await self.db.commit()
