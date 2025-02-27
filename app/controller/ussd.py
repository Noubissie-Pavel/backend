from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.ussd import Ussd
from app.schemas.ussd import UssdCreate, UssdUpdate


def create_ussd(db: Session, ussd_data: UssdCreate):
    db_ussd = Ussd(
        code=ussd_data.code,
        description=ussd_data.description,
        is_active=ussd_data.is_active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    try:
        db.add(db_ussd)
        db.commit()
        db.refresh(db_ussd)
        return db_ussd
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Operator with name {ussd_data.operator_name} already exists.")


# def get_ussd(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Ussd).offset(skip).limit(limit).all()
#

async def get_ussd(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Ussd).offset(skip).limit(limit))
    return await result.scalars().fetchall()


def get_ussd_by_id(db: Session, ussd_id: int):
    return db.query(Ussd).filter(Ussd.id == ussd_id).first()


def update_ussd(db: Session, ussd_id: int, ussd_data: UssdUpdate):
    db_ussd = db.query(Ussd).filter(Ussd.id == ussd_id).first()
    if db_ussd:
        db_ussd.code = ussd_data.code or db_ussd.code
        db_ussd.description = ussd_data.description or db_ussd.description
        db_ussd.is_active = ussd_data.is_active or db_ussd.is_active
        db_ussd.updated_at = datetime.now()

        try:
            db.commit()
            db.refresh(db_ussd)
            return db_ussd
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Operator with name {ussd_data.operator_name} already exists.")
    return None


def delete_ussd(db: Session, ussd_id: int):
    db_ussd = db.query(Ussd).filter(
        Ussd.id == ussd_id).first()
    if db_ussd:
        db.delete(db_ussd)
        db.commit()
        return db_ussd
    return None
