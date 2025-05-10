from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import text

from database import async_session_maker
from src import redis_manager
from src.api import routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
            print("### PG database startup success ###")

        await redis_manager.connect()
        FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
        print("### Redis connect success ###")
    except Exception as e:
        print(f"### Error during startup: {e} ###")
        raise
    yield
    await redis_manager.close()
    print("### Redis disconnect success ###")
    print("### Databases shutdown success ###")


app = FastAPI(lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def root_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")


for rout in routers:
    app.include_router(rout)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
