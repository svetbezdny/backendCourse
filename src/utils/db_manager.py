from src.repos.bookings import BookingsRepos
from src.repos.hotels import HotelsRepos
from src.repos.rooms import RoomsRepos
from src.repos.users import UsersRepos


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self) -> "DBManager":
        self.session = self.session_factory()

        self.hotels = HotelsRepos(self.session)
        self.rooms = RoomsRepos(self.session)
        self.users = UsersRepos(self.session)
        self.bookings = BookingsRepos(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, traceback) -> None:
        await self.session.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()
