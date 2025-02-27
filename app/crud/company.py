from datetime import datetime

from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanyCreate


def create_company(db: Session, company: CompanyCreate):
    db_company = Company(
        name=company.name,
        description=company.description,
        is_active=company.is_active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()
