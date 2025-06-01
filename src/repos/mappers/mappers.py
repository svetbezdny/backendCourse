from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repos.mappers.base import DataMapper
from src.schemas.bookings import BookingsAdd, BookingsRequest
from src.schemas.facilities import Facility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingsDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = BookingsAdd  # BookingsRequest


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
