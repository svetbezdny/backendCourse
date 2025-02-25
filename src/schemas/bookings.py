from datetime import date

from pydantic import BaseModel


class BookingsRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingsAdd(BookingsRequest):
    user_id: int
    price: int
