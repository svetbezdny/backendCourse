from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepos
from src.schemas.rooms import Room


class RoomsRepos(BaseRepos):
    model = RoomsOrm
    schema = Room
