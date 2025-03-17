from pydantic import BaseModel


class Facility(BaseModel):
    id: int
    title: str
