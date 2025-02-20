from fastapi import APIRouter, HTTPException, status

from src.database import async_db_conn
from src.repos.hotels import HotelsRepos
from src.repos.rooms import RoomsRepos
from src.schemas.rooms import Room, RoomAdd, RoomPATCH, RoomPUT

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms", response_model=list[Room])
async def get_all_rooms(db: async_db_conn, hotel_id: int):
    rooms = await RoomsRepos(db).get_all(hotel_id=hotel_id)
    if not rooms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No rooms found"
        )
    return rooms


@router.get("/{hotel_id}/rooms/{room_id}", response_model=Room)
async def get_room(db: async_db_conn, hotel_id: int, room_id: int):
    room = await RoomsRepos(db).get_one_or_none(hotel_id=hotel_id, id=room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found",
        )
    return room


@router.post("/{hotel_id}/rooms", status_code=status.HTTP_201_CREATED)
async def create_room(db: async_db_conn, room_data: RoomAdd):
    hotel = await HotelsRepos(db).get_one_or_none(id=room_data.hotel_id)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {room_data.hotel_id} not found",
        )
    room = await RoomsRepos(db).add(room_data)
    await db.commit()
    return {
        "transaction": "Successful",
        "data": room,
    }


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: async_db_conn, hotel_id: int, room_id: int):
    room = await RoomsRepos(db).get_one_or_none(hotel_id=hotel_id, id=room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found",
        )
    await RoomsRepos(db).delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {
        "transaction": f"Room with id {room_id} was deleted",
    }


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(db: async_db_conn, hotel_id: int, room_id: int, room_data: RoomPUT):
    room = await RoomsRepos(db).get_one_or_none(hotel_id=hotel_id, id=room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found",
        )
    await RoomsRepos(db).edit(room_data, id=room_id)
    await db.commit()
    return {
        "transaction": f"Room with id {room_id} was updated",
    }


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
    db: async_db_conn, hotel_id: int, room_id: int, room_data: RoomPATCH
):
    room = await RoomsRepos(db).get_one_or_none(hotel_id=hotel_id, id=room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found",
        )
    await RoomsRepos(db).edit(
        room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id
    )
    await db.commit()
    return {
        "transaction": f"Room with id {room_id} was updated",
    }
