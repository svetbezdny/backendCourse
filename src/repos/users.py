from pydantic import EmailStr
from sqlalchemy import select

from src.exceptions import UserAlreadyExistException
from src.models.users import UsersOrm
from src.repos.base import BaseRepos
from src.repos.mappers.mappers import UsersDataMapper
from src.schemas.users import UserWithHashedPassword


class UsersRepos(BaseRepos):
    model = UsersOrm
    mapper = UsersDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        res = result.scalar_one_or_none()
        if res:
            return UserWithHashedPassword.model_validate(res, from_attributes=True)
        return None

    async def get_one(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        if len(result.all()) > 0:
            raise UserAlreadyExistException
