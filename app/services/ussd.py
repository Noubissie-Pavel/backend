from sqlalchemy.orm import Session

from app.controller.ussd import create_ussd, get_ussd, get_ussd_by_id, update_ussd, delete_ussd
from app.schemas.ussd import UssdCreate, UssdUpdate


def create_ussd_service(db: Session, ussd_data: UssdCreate):
    return create_ussd(db=db, ussd_data=ussd_data)


async def get_ussd_service(db: Session, skip: int = 0, limit: int = 100):
    return await get_ussd(db=db, skip=skip, limit=limit)


def get_ussd_by_id_service(db: Session, ussd_id: int):
    return get_ussd_by_id(db=db, ussd_id=ussd_id)


def update_ussd_service(db: Session, ussd_id: int, ussd_data: UssdUpdate):
    return update_ussd(db=db, ussd_id=ussd_id, ussd_data=ussd_data)


def delete_ussd_service(db: Session, ussd_id: int):
    return delete_ussd(db=db, ussd_id=ussd_id)
