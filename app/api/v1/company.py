from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.company import CompanyCreate, Company
from app.services.company import create_company_service, get_companies_service

company_v1 = APIRouter()


@company_v1.post("/company", response_model=Company)
def create_company_endpoint(company: CompanyCreate, db: Session = Depends(get_db)):
    return create_company_service(db=db, company=company)


@company_v1.get("/companies", response_model=list[Company])
def get_users_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), request: Request = None):
    request.state.response_message = 'Testing get_companies_service response message'
    return get_companies_service(db=db, skip=skip, limit=limit)
