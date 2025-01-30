from fastapi import FastAPI, HTTPException, status
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_db_conn
from src.fake import hotels
from src.models.hotels import HotelsOrm
from src.repos.hotels import HotelsRepos
from src.schemas.hotels import Hotels

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


@app.post("/hotels", status_code=status.HTTP_201_CREATED)
async def create_hotel(db: async_db_conn, hotel_data: Hotels) -> dict:
    hotel = await HotelsRepos(db).add(
        title=hotel_data.title, location=hotel_data.location
    )
    await db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful",
        "data": {col.name: getattr(hotel, col.name) for col in hotel.__table__.columns},
    }


@app.delete("/hotels/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(hotel_id: int):
    for idx, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            hotels.pop(idx)
            break


@app.put("/hotels/{hotel_id}")
async def put_hotel(
    hotel_id: int,
    title: str,
    name: str,
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"message": f"The hotel {name} has been changed"}
        else:
            raise HTTPException(status_code=404, detail="Hotel was not found")


@app.patch("/hotels/{hotel_id}")
async def patch_hotel(
    hotel_id: int,
    title: str | None = None,
    name: str | None = None,
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
            return {"message": f"The hotel with id {hotel_id} has been changed"}
        else:
            raise HTTPException(status_code=404, detail="Hotel was not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
