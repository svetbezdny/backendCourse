from sqlalchemy import insert, select
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

    async def add(self, **kwargs):
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
