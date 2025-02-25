from fastapi import FastAPI

from src.api.auth import router as auth_router
from src.api.bookings import router as bookings_router
from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
