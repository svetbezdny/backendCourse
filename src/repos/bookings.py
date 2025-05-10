from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepos
from src.repos.mappers.mappers import BookingsDataMapper


class BookingsRepos(BaseRepos):
    model = BookingsOrm
    mapper = BookingsDataMapper
