from fastapi import APIRouter, HTTPException, Response, status

from src.api.dependencies import UserIdDep
from src.database import async_db_conn
from src.repos.users import UsersRepos
from src.schemas.users import UserAdd, UserRequest, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authorization and authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(db: async_db_conn, data: UserRequestAdd):
    existing_user = await UsersRepos(db).get_one_or_none(email=data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
        )
    hashed_password = AuthService().hash_password(data.password)
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


@router.post("/login")
async def login_user(db: async_db_conn, data: UserRequest, response: Response):
    user = await UsersRepos(db).get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user with this email not registered",
        )
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    access_token = AuthService().create_jwt_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(db: async_db_conn, user_id: UserIdDep):
    user_data = await UsersRepos(db).get_one_or_none(id=user_id)
    if user_data:
        return user_data


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie("access_token")
