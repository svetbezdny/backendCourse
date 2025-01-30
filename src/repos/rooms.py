from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepos


class RoomsRepos(BaseRepos):
    model = RoomsOrm
