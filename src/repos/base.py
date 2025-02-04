from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepos:
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, *args, **kawrgs):
        query = select(self.model)
        result = await self.session.scalars(query)

        return result.all()

    async def get_one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
