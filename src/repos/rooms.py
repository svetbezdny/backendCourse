from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepos
from src.schemas.rooms import Room


class RoomsRepos(BaseRepos):
    model = RoomsOrm
    schema = Room

    async def get_all(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.scalars(query)
        return list(
            map(
                lambda x: self.schema.model_validate(x, from_attributes=True),
                result.all(),
            )
        )
