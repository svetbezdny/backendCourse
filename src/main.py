import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Path
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import text

from database import async_session_maker
from src import redis_manager
from src.api import routers

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
            logging.info("### PG database startup success ###")

        await redis_manager.connect()
        FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
        logging.info("### Redis connect success ###")
    except Exception as e:
        logging.error(f"### Error during startup: {e} ###")
        raise
    yield
    await redis_manager.close()
    logging.info("### Redis disconnect success ###")
    logging.info("### Databases shutdown success ###")


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="src/templates"), name="static")

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def root_redirect() -> RedirectResponse:
    return RedirectResponse(url="/static/index.html", status_code=302)


for rout in routers:
    app.include_router(rout)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
