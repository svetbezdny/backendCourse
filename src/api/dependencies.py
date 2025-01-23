from fastapi import Query


async def pagination(
    page: int = Query(1, ge=1),
    per_page: int = Query(3, ge=1, le=10),
) -> dict:
    return {"page": page, "per_page": per_page}
