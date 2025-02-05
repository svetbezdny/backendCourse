from fastapi import FastAPI, HTTPException, status

from src.api.dependencies import PaginationDep
from src.database import async_db_conn
from src.repos.hotels import HotelsRepos
from src.schemas.hotels import HotelPATCH, Hotels

app = FastAPI()


@app.get("/hotels", response_model=list[Hotels])
async def get_hotels(
    db: async_db_conn,
    pagination: PaginationDep,
    title: str | None = None,
    location: str | None = None,
):
    hotels = await HotelsRepos(db).get_all(
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


@app.get("/{hotel_id}", response_model=Hotels)
async def get_hotel(db: async_db_conn, hotel_id: int):
    hotel = await HotelsRepos(db).get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    return hotel


@app.post("/hotels")
async def create_hotel(db: async_db_conn, hotel_data: Hotels):
    hotel = await HotelsRepos(db).add(hotel_data)
    await db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful",
        "data": hotel,
    }


@app.delete("/hotels/{hotel_id}")
async def delete_hotel(db: async_db_conn, hotel_id: int):
    hotel = await HotelsRepos(db).get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    await HotelsRepos(db).delete(id=hotel_id)
    await db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": f"Hotel with id {hotel_id} was deleted",
    }


@app.put("/hotels/{hotel_id}")
async def put_hotel(
    db: async_db_conn,
    hotel_data: Hotels,
    hotel_id: int,
):
    hotel = await HotelsRepos(db).get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    await HotelsRepos(db).edit(hotel_data, id=hotel_id)
    await db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": f"Hotel with id {hotel_id} was updated",
    }


@app.patch("/hotels/{hotel_id}")
async def patch_hotel(
    db: async_db_conn,
    hotel_data: HotelPATCH,
    hotel_id: int,
):
    hotel = await HotelsRepos(db).get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found",
        )
    await HotelsRepos(db).edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": f"Hotel with id {hotel_id} was updated",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
