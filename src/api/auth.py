from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext

from src.database import async_db_conn
from src.repos.users import UsersRepos
from src.schemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Authorization and authentication"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(db: async_db_conn, data: UserRequestAdd):
    existing_user = await UsersRepos(db).get_one_or_none(email=data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
        )
    hashed_password = pwd_context.hash(data.password)
    new_user = UserAdd(
        first_name=data.first_name,
        last_name=data.last_name,
        age=data.age,
        city=data.city,
        email=data.email,
        hashed_password=hashed_password,
    )
    await UsersRepos(db).add(new_user)
    await db.commit()
    return {"transaction": "Successful"}
