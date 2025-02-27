import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.company import get_companies as crud_get_companies, \
    get_company_by_id as crud_get_company_by_id, update_company as crud_update_company, \
    delete_company as crud_delete_company, create_company
from app.schemas.company import CompanyCreate, Company, CompanyUpdate

logger = logging.getLogger(__name__)


async def create_company_service(db: AsyncSession, company_data: CompanyCreate) -> Company:
    try:
        company = await create_company(db, company_data)
        if company is None:
            raise HTTPException(status_code=400, detail=f"Company with name '{company_data.name}' already exists.")
        return company
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_company_service: {str(e)}")
        raise


async def get_companies_service(db: Session, skip: int = 0, limit: int = 100):
    return await crud_get_companies(db, skip, limit)


async def get_company_by_id_service(db: AsyncSession, company_id: int) -> Company:
    result = await crud_get_company_by_id(db, company_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Company with id {company_id} not found.")
    return result


async def update_company_service(db: AsyncSession, company_id: int, company_data: CompanyUpdate) -> Company:
    existing_company = await crud_get_company_by_id(db, company_id)
    if existing_company is None:
        raise HTTPException(status_code=404, detail=f"Company with id {company_id} not found.")
    return await crud_update_company(db, company_id, company_data)


async def delete_company_service(db: AsyncSession, company_id: int) -> Company:
    existing_company = await crud_get_company_by_id(db, company_id)
    if existing_company is None:
        raise HTTPException(status_code=404, detail=f"Company with id {company_id} not found.")
    return await crud_delete_company(db, company_id)
