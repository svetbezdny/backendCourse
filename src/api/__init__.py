from api.auth import router as auth_router
from api.bookings import router as bookings_router
from api.facilities import router as facilities_router
from api.hotels import router as hotels_router
from api.rooms import router as rooms_router

routers = [
    auth_router,
    bookings_router,
    facilities_router,
    hotels_router,
    rooms_router,
]

__all__ = ["routers"]
