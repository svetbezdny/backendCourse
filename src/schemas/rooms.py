from pydantic import BaseModel


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomPUT(BaseModel):
    title: str
    description: str
    price: int
    quantity: int


class RoomPATCH(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
