from typing import Optional

import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int, db: int = 0) -> None:
        self.host = host
        self.port = port
        self.db = db
        self.redis: redis.Redis = None  # type: ignore

    async def connect(self):
        self.redis = await redis.Redis(host=self.host, port=self.port, db=self.db)

    async def set(self, key: str, value: str, expire: Optional[int] = None) -> None:
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()
