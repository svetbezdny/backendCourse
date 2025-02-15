from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepos
from src.schemas.hotels import Hotel


class HotelsRepos(BaseRepos):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
        self,
        title: str | None = None,
        location: str | None = None,
        limit: int = 1,
        offset: int = 5,
    ) -> list[Hotel]:
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
        return list(
            map(
                lambda x: self.schema.model_validate(x, from_attributes=True),
                hotels_query.all(),
            )
        )
