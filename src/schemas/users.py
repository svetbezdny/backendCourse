from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRequest(BaseModel):
    email: EmailStr
    password: str


class UserRequestAdd(UserRequest):
    first_name: str
    last_name: Optional[str] = None
    age: int = Field(ge=0, lt=150)
    city: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "age": "30",
                "city": "New York",
                "email": "john_doe@example.com",
                "password": "MyPaSs123!#",
            }
        }
    )


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


class UserWithHashedPassword(User):
    hashed_password: str
