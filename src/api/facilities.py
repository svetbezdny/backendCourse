from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache

from src.api.dependencies import async_db_conn
from src.config import settings
from src.exceptions import ObjectNotFoundException
from src.schemas.facilities import Facility
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("", response_model=list[Facility])
@cache(expire=settings.REDIS_EXPIRE_SEC)
async def get_all_facilities(db: async_db_conn):
    try:
        facilities_db = await FacilityService(db).get_facilities()
        return facilities_db
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No facilities found"
        )


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_facility(db: async_db_conn, facility_data: Facility):
    facility = await FacilityService(db).create_facility(facility_data)
    return {
        "message": "Successful",
        "data": facility,
    }
