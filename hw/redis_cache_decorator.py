import sys
from functools import wraps
from pathlib import Path
from typing import Optional

import orjson
from fastapi import FastAPI, Query

sys.path.append(str(Path(__file__).parents[1]))


from src import redis_manager
from src.config import settings

app = FastAPI()


def memo(expire: Optional[int] = None):
    def wmemo(func):
        @wraps(func)
        async def imemo(*args, **kwargs):
            request_params_lst = [arg for arg in args]
            for k, v in kwargs.items():
                if k != "request":
                    request_params_lst.append(f"{k}_{v}")
            redis_key = "_".join(request_params_lst)

            await redis_manager.connect()
            cache_data = await redis_manager.get(key=redis_key)
            if cache_data:
                await redis_manager.close()
                return orjson.loads(cache_data)

            result = await func(*args, **kwargs)

            await redis_manager.set(
                key=redis_key, value=orjson.dumps(result).decode("utf-8"), expire=expire
            )

            await redis_manager.close()
            return result

        return imemo

    return wmemo


@app.get("/fib")
@memo(expire=settings.REDIS_EXPIRE_SEC)
async def fibonacci(n: int = Query(ge=0, le=93)) -> dict:
    a, b = 0, 1
    if n == 0:
        return {"result": 0}
    elif n == 1:
        return {"result": b}
    else:
        for i in range(1, n):
            a, b = b, a + b
        return {"result": b}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("redis_cache_decorator:app", reload=True)
