import logging
import traceback
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.agency import Agency
from app.schemas.agency import AgencyCreate, AgencyUpdate

logger = logging.getLogger(__name__)


async def create_agency(db: AsyncSession, agency_data: AgencyCreate):
    db_agency = Agency(**agency_data.dict(), created_at=datetime.now(), updated_at=datetime.now())
    try:
        db.add(db_agency)
        await db.commit()
        await db.refresh(db_agency)
        return db_agency
    except IntegrityError as e:
        await db.rollback()
        if "unique constraint" in str(e).lower():
            logger.error(
                f"Agency with name {agency_data.name}  or agency_code {agency_data.agency_code} already exists.")
            return None
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


async def get_agencies(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Agency).offset(skip).limit(limit))
    return result.scalars().all()


async def get_agency_by_id(db: AsyncSession, agency_id: int):
    result = await db.execute(select(Agency).filter(Agency.id == agency_id))
    return result.scalars().first()


async def update_agency(db: AsyncSession, agency_id: int, agency_data: AgencyUpdate):
    result = await db.execute(select(Agency).filter(Agency.id == agency_id))
    db_agency = result.scalars().first()
    if db_agency:
        db_agency.name = agency_data.name or db_agency.name
        db_agency.agency_code = agency_data.agency_code or db_agency.agency_code
        db_agency.description = agency_data.description or db_agency.description
        db_agency.is_active = agency_data.is_active or db_agency.is_active
        db_agency.updated_at = datetime.now()

        try:
            await db.commit()
            await db.refresh(db_agency)
            return db_agency
        except IntegrityError:
            await db.rollback()
            raise ValueError(
                f"Agency with name {agency_data.name}  or agency_code {agency_data.agency_code} already exists.")
    return None


async def delete_agency(db: AsyncSession, agency_id: int):
    result = await db.execute(select(Agency).filter(Agency.id == agency_id))
    db_agency = result.scalars().first()
    if db_agency:
        await db.delete(db_agency)
        await db.commit()
        return db_agency
    return None
