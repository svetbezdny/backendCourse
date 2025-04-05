from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repos.base import BaseRepos
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepos(BaseRepos):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepos(BaseRepos):
    model = RoomsFacilitiesOrm
    schema = RoomFacility
