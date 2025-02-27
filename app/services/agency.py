import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.agency import get_agencies as crud_get_agencies, \
    get_agency_by_id as crud_get_agency_by_id, update_agency as crud_update_agency, \
    delete_agency as crud_delete_agency, create_agency
from app.schemas.agency import AgencyCreate, Agency, AgencyUpdate

logger = logging.getLogger(__name__)


async def create_agency_service(db: AsyncSession, agency_data: AgencyCreate) -> Agency:
    try:
        agency = await create_agency(db, agency_data)
        if agency is None:
            raise HTTPException(status_code=400,
                                detail=f"Agency with name '{agency_data.name}' or agency_code '{agency_data.agency_code}' already exists.")
        return agency
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_agency_service: {str(e)}")
        raise


async def get_agencies_service(db: Session, skip: int = 0, limit: int = 100):
    return await crud_get_agencies(db, skip, limit)


async def get_agency_by_id_service(db: AsyncSession, agency_id: int) -> Agency:
    result = await crud_get_agency_by_id(db, agency_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Agency with id {agency_id} not found.")
    return result


async def update_agency_service(db: AsyncSession, agency_id: int, agency_data: AgencyUpdate) -> Agency:
    existing_agency = await crud_get_agency_by_id(db, agency_id)
    if existing_agency is None:
        raise HTTPException(status_code=404, detail=f"Agency with id {agency_id} not found.")
    return await crud_update_agency(db, agency_id, agency_data)


async def delete_agency_service(db: AsyncSession, agency_id: int) -> Agency:
    existing_agency = await crud_get_agency_by_id(db, agency_id)
    if existing_agency is None:
        raise HTTPException(status_code=404, detail=f"Agency with id {agency_id} not found.")
    return await crud_delete_agency(db, agency_id)
