from datetime import date

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import async_db_conn
from src.exceptions import (HotelDoesNotExistException,
                            MismatchedDatesException,
                            RoomDoesNotExistException)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_all_rooms(
    db: async_db_conn, hotel_id: int, date_from: date, date_to: date
):
    try:
        return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)
    except MismatchedDatesException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.detail)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: async_db_conn, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except RoomDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )


@router.post("/{hotel_id}/rooms", status_code=status.HTTP_201_CREATED)
async def create_room(db: async_db_conn, hotel_id: int, room_data: RoomAddRequest):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
        return {
            "message": "Successful",
            "data": room,
        }
    except HotelDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
    db: async_db_conn, hotel_id: int, room_id: int, room_data: RoomAddRequest
):
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
        return {
            "message": f"Room with id {room_id} was updated",
        }
    except RoomDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
    db: async_db_conn, hotel_id: int, room_id: int, room_data: RoomPatchRequest
):
    try:
        await RoomService(db).partial_edit_room(hotel_id, room_id, room_data)
        return {
            "message": f"Room with id {room_id} was updated",
        }
    except RoomDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: async_db_conn, hotel_id: int, room_id: int):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
        return {
            "message": f"Room with id {room_id} was deleted",
        }
    except RoomDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )
