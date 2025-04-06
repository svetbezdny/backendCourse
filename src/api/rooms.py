from datetime import date

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import async_db_conn
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import (RoomAdd, RoomAddRequest, RoomPatch,
                               RoomPatchRequest)

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_all_rooms(
    db: async_db_conn, hotel_id: int, date_from: date, date_to: date
):
    rooms = await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )
    if not rooms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No rooms found"
        )
    return rooms


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: async_db_conn, hotel_id: int, room_id: int):
    room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found",
        )
    return room


@router.post("/{hotel_id}/rooms", status_code=status.HTTP_201_CREATED)
async def create_room(db: async_db_conn, hotel_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    hotel = await db.hotels.get_one_or_none(id=_room_data.hotel_id)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {_room_data.hotel_id} not found",
        )
    room = await db.rooms.add(_room_data)

    rooms_fac_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_fac_data)
    await db.commit()
    return {
        "transaction": "Successful",
        "data": room,
    }


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
    db: async_db_conn, hotel_id: int, room_id: int, room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {
        "transaction": f"Room with id {room_id} was updated",
    }


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
    db: async_db_conn, hotel_id: int, room_id: int, room_data: RoomPatchRequest
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found",
        )
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {
        "transaction": f"Room with id {room_id} was updated",
    }


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: async_db_conn, hotel_id: int, room_id: int):
    room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found",
        )
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {
        "transaction": f"Room with id {room_id} was deleted",
    }
