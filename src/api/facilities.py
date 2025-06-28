from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache

from src.api.dependencies import async_db_conn
from src.config import settings
from src.schemas.facilities import Facility

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("", response_model=list[Facility])
@cache(expire=settings.REDIS_EXPIRE_SEC)
async def get_all_facilities(db: async_db_conn):
    facilities_db = await db.facilities.get_all()
    if not facilities_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No facilities found"
        )

    return facilities_db


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_facility(db: async_db_conn, facility_data: Facility):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {
        "message": "Successful",
        "data": facility,
    }
