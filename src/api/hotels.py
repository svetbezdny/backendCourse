from datetime import date

from fastapi import APIRouter, HTTPException, Query, status
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, async_db_conn
from src.config import settings
from src.exceptions import HotelDoesNotExistException, MismatchedDatesException
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("", response_model=list[Hotel])
@cache(expire=settings.REDIS_EXPIRE_SEC)
async def get_hotels(
    db: async_db_conn,
    pagination: PaginationDep,
    title: str | None = None,
    location: str | None = None,
    date_from: date = Query(),
    date_to: date = Query(),
):
    try:
        return await HotelService(db).get_filtered_by_time(
            pagination, title, location, date_from=date_from, date_to=date_to
        )
    except MismatchedDatesException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.detail)


@router.get("/{hotel_id}", response_model=Hotel)
async def get_hotel(db: async_db_conn, hotel_id: int):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except HotelDoesNotExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_hotel(db: async_db_conn, hotel_data: HotelAdd):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {
        "message": "Successful",
        "data": hotel,
    }


@router.put("/{hotel_id}")
async def put_hotel(db: async_db_conn, hotel_data: HotelAdd, hotel_id: int):
    result = await HotelService(db).put_hotel(hotel_data, hotel_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    return {
        "message": f"Hotel with id {hotel_id} was updated",
    }


@router.patch("/{hotel_id}")
async def patch_hotel(db: async_db_conn, hotel_data: HotelPATCH, hotel_id: int):
    result = await HotelService(db).patch_hotel(hotel_data, hotel_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    return {
        "message": f"Hotel with id {hotel_id} was updated",
    }


@router.delete("/{hotel_id}")
async def delete_hotel(db: async_db_conn, hotel_id: int):
    result = await HotelService(db).delete_hotel(hotel_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    return {
        "message": f"Hotel with id {hotel_id} was deleted",
    }
