from typing import Annotated, AsyncGenerator, Optional

from fastapi import Depends, HTTPException, Query, Request, status
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


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


def get_current_user_id(
    access_token: Annotated[str, Depends(get_token)],
) -> Optional[int]:
    jwt_data = AuthService().decode_jwt_token(access_token)
    return jwt_data.get("user_id")


async def get_db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


PaginationDep = Annotated[PaginationParams, Depends()]
UserIdDep = Annotated[int, Depends(get_current_user_id)]
async_db_conn = Annotated[DBManager, Depends(get_db)]
