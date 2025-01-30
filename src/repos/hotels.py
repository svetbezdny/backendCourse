from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepos


class HotelsRepos(BaseRepos):
    model = HotelsOrm

    async def get_all(
        self,
        title: str | None = None,
        location: str | None = None,
        limit: int = 1,
        offset: int = 5,
    ):
        hotels_query = select(self.model)
        if title is not None:
            hotels_query = hotels_query.where(self.model.title.ilike(f"%{title}%"))
        if location is not None:
            hotels_query = hotels_query.where(
                self.model.location.ilike(f"%{location}%")
            )

        hotels_query = await self.session.scalars(
            hotels_query.limit(limit).offset(limit * (offset - 1))
        )
        return hotels_query.all()
