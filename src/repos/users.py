from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersOrm
from src.repos.base import BaseRepos
from src.schemas.users import User, UserWithHashedPassword


class UsersRepos(BaseRepos):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        res = result.scalar_one_or_none()
        if res:
            return UserWithHashedPassword.model_validate(res, from_attributes=True)
        return None
