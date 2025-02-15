from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRequestAdd(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    age: int = Field(ge=0, lt=150)
    city: Optional[str] = None
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    first_name: str
    last_name: Optional[str]
    age: int = Field(ge=0, lt=150)
    city: Optional[str] = None
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr
