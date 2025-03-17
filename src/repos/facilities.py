from src.models.facilities import FacilitiesOrm
from src.repos.base import BaseRepos
from src.schemas.facilities import Facility


class FacilitiesRepos(BaseRepos):
    model = FacilitiesOrm
    schema = Facility
