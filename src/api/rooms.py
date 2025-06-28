from datetime import date

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import async_db_conn
from src.exceptions import (HotelDoesNotExistException,
                            MismatchedDatesException,
                            RoomDoesNotExistException)
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import (RoomAdd, RoomAddRequest, RoomPatch,
                               RoomPatchRequest)

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_all_rooms(
    db: async_db_conn, hotel_id: int, date_from: date, date_to: date
):
    try:
        rooms = await db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        return rooms
    except MismatchedDatesException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.detail)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: async_db_conn, hotel_id: int, room_id: int):
    try:
        room = await db.rooms.get_one(hotel_id=hotel_id, id=room_id)
        return room
    except RoomDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )


@router.post("/{hotel_id}/rooms", status_code=status.HTTP_201_CREATED)
async def create_room(db: async_db_conn, hotel_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        await db.hotels.get_one(id=_room_data.hotel_id)
    except HotelDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )
    room = await db.rooms.add(_room_data)

    rooms_fac_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)  # type: ignore
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_fac_data)
    await db.commit()
    return {
        "message": "Successful",
        "data": room,
    }


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
    db: async_db_conn, hotel_id: int, room_id: int, room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        await db.rooms.edit(_room_data, id=room_id)
    except RoomDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )

    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {
        "message": f"Room with id {room_id} was updated",
    }


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
    db: async_db_conn, hotel_id: int, room_id: int, room_data: RoomPatchRequest
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    try:
        await db.rooms.get_one(hotel_id=hotel_id, id=room_id)
    except RoomDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {
        "message": f"Room with id {room_id} was updated",
    }


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: async_db_conn, hotel_id: int, room_id: int):
    try:
        await db.rooms.get_one(hotel_id=hotel_id, id=room_id)
    except RoomDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {
        "message": f"Room with id {room_id} was deleted",
    }
