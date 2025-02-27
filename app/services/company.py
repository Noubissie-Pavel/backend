from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from app.controller.company import create_company as crud_create_company
from app.controller.company import get_companies as crud_get_companies
from app.schemas.company import CompanyCreate


async def create_company_service(db: Session, company: CompanyCreate):
    return await crud_create_company(db=db, company=company)


async def get_companies_service(db: Session, skip: int = 0, limit: int = 100):
    return await crud_get_companies(db=db, skip=skip, limit=limit)
