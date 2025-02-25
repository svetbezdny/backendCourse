from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepos
from src.schemas.bookings import BookingsRequest


class BookingsRepos(BaseRepos):
    model = BookingsOrm
    schema = BookingsRequest
