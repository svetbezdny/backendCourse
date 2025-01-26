from pydantic import BaseModel


class Hotels(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None
