from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import PaginationDep, async_db_conn
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/", response_model=list[Hotel])
async def get_hotels(
    db: async_db_conn,
    pagination: PaginationDep,
    title: str | None = None,
    location: str | None = None,
):
    hotels = await db.hotels.get_all(
        title=title,
        location=location,
        limit=pagination.per_page,
        offset=pagination.page,
    )
    if not hotels:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No hotels found"
        )
    return hotels


@router.get("/{hotel_id}", response_model=Hotel)
async def get_hotel(db: async_db_conn, hotel_id: int):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    return hotel


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_hotel(db: async_db_conn, hotel_data: HotelAdd):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {
        "transaction": "Successful",
        "data": hotel,
    }


@router.delete("/{hotel_id}")
async def delete_hotel(db: async_db_conn, hotel_id: int):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {
        "transaction": f"Hotel with id {hotel_id} was deleted",
    }


@router.put("/{hotel_id}")
async def put_hotel(db: async_db_conn, hotel_data: HotelAdd, hotel_id: int):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {
        "transaction": f"Hotel with id {hotel_id} was updated",
    }


@router.patch("/{hotel_id}")
async def patch_hotel(db: async_db_conn, hotel_data: HotelPATCH, hotel_id: int):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {
        "transaction": f"Hotel with id {hotel_id} was updated",
    }
