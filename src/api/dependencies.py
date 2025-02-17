from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request, status
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int, Query(ge=1)] = 1
    per_page: Annotated[int, Query(ge=1, le=20)] = 5


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token")
    if access_token:
        return access_token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The token is not provided",
    )


def get_current_user_id(access_token: Annotated[str, Depends(get_token)]) -> int:
    jwt_data = AuthService().decode_jwt_token(access_token)
    return jwt_data.get("user_id")


PaginationDep = Annotated[PaginationParams, Depends()]
UserIdDep = Annotated[int, Depends(get_current_user_id)]
