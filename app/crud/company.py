import logging
import traceback
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

logger = logging.getLogger(__name__)


async def create_company(db: AsyncSession, company_data: CompanyCreate):
    db_company = Company(**company_data.dict(), created_at=datetime.now(), updated_at=datetime.now())
    try:
        db.add(db_company)
        await db.commit()
        await db.refresh(db_company)
        return db_company
    except IntegrityError as e:
        await db.rollback()
        if "unique constraint" in str(e).lower():
            logger.error(f"Company with name {company_data.name} already exists.")
            return None
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


async def get_companies(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Company).offset(skip).limit(limit))
    return result.scalars().all()


async def get_company_by_id(db: AsyncSession, company_id: int):
    result = await db.execute(select(Company).filter(Company.id == company_id))
    return result.scalars().first()


async def update_company(db: AsyncSession, company_id: int, company_data: CompanyUpdate):
    result = await db.execute(select(Company).filter(Company.id == company_id))
    db_company = result.scalars().first()
    if db_company:
        db_company.name = company_data.name or db_company.name
        db_company.description = company_data.description or db_company.description
        db_company.is_active = company_data.is_active or db_company.is_active
        db_company.updated_at = datetime.now()

        try:
            await db.commit()
            await db.refresh(db_company)
            return db_company
        except IntegrityError:
            await db.rollback()
            raise ValueError(f"Company with name {company_data.name} already exists.")
    return None


async def delete_company(db: AsyncSession, company_id: int):
    result = await db.execute(select(Company).filter(Company.id == company_id))
    db_company = result.scalars().first()
    if db_company:
        await db.delete(db_company)
        await db.commit()
        return db_company
    return None
