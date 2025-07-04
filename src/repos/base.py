from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.exceptions import ObjectNotFoundException
from src.repos.mappers.base import DataMapper


class BaseRepos:
    model = Base
    mapper = DataMapper

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.scalars(query)
        return list(
            map(
                lambda x: self.mapper.map_to_domain_entity(x),
                result.all(),
            )
        )

    async def get_one(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        try:
            res = result.scalar_one()
            return self.mapper.map_to_domain_entity(res)
        except NoResultFound:
            raise ObjectNotFoundException

    async def get_one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        res = result.scalar_one_or_none()
        if res:
            return self.mapper.map_to_domain_entity(res)
        return None

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        res = result.scalar_one_or_none()
        if res:
            return self.mapper.map_to_domain_entity(res)
        return None

    async def add_bulk(self, data: Sequence[BaseModel]):
        stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(stmt)

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
