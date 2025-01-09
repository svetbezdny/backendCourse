from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@app.get("/hotels")
async def get_hotels(
    id: int | None = None,
    title: str | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=3, ge=1, le=len(hotels)),
) -> list[dict]:
    res = []
    for i in hotels:
        if id and title:
            if i["id"] == id and i["title"] == title:
                res.append(i)
        elif id:
            if i["id"] == id:
                res.append(i)
        elif title:
            if i["title"] == title:
                res.append(i)
        else:
            res.append(i)
    return res[(page - 1) * per_page : page * per_page]


@app.post("/hotels", status_code=201)
async def create_hotel(title: str, name: str) -> dict:
    hotels.append({"id": hotels[-1]["id"] + 1, "title": title, "name": name})
    return {"message": f"The hotel {name} has been added"}


@app.delete("/hotels/{hotel_id}", status_code=204)
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
def patch_hotel(
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
