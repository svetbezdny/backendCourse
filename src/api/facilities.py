from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import async_db_conn
from src.schemas.facilities import Facility

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("/", response_model=list[Facility])
async def get_all_facilities(db: async_db_conn):
    all_facilities = await db.facilities.get_all()
    if not all_facilities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No facilities found"
        )
    return all_facilities


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_facility(db: async_db_conn, facility_data: Facility):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {
        "transaction": "Successful",
        "data": facility,
    }
