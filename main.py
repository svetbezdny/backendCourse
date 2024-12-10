import uvicorn
from fastapi import Body, FastAPI, Query

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi"},
    {"id": 2, "title": "Dubai", "name": "Dubai"},
]


@app.get("/hotels")
def get_hotels(
    id: int | None = None,
    title: str | None = Query(default=None, description="Город"),
) -> list:
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
    return res or ["no data"]


@app.post("/hotels")
def create_hotel(title: str = Body(embed=True)):
    hotels.append({"id": hotels[-1]["id"] + 1, "title": title})
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    for idx, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            hotels.pop(idx)
            break
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def put_hotel(
    hotel_id: int,
    title: str = Body(embed=True),
    name: str = Body(embed=True),
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
        return {"error": "hotel not found"}, 404


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
            return {"status": "OK"}
        return {"erorr": "hotel not found"}, 404


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
