from src.models.users import UsersOrm
from src.repos.base import BaseRepos
from src.schemas.users import User


class UsersRepos(BaseRepos):
    model = UsersOrm
    schema = User
