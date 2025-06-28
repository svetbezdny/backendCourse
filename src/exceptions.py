class NabronirovalException(Exception):
    detail = "Unknown error"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Object not found"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "There are no free rooms"


class UserAlreadyExistException(NabronirovalException):
    detail = "The user already exists"


class HotelDoesNotExistException(NabronirovalException):
    detail = "The hotel does not exist"


class MismatchedDatesException(NabronirovalException):
    detail = "Check-in date later than check-out date"


class RoomDoesNotExistException(NabronirovalException):
    detail = "The room does not exist"
