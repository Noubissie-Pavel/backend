from sqlalchemy.orm import Session

from app.controller.telecom_operator import create_telecom_operator, get_telecom_operators, get_telecom_operator_by_id
from app.schemas.telecom_operator import TelecomOperatorCreate


def create_telecom_operator_service(db: Session, telecom_operator: TelecomOperatorCreate):
    return create_telecom_operator(db=db, telecom_operator=telecom_operator)


def get_telecom_operators_service(db: Session, skip: int = 0, limit: int = 100):
    return get_telecom_operators(db=db, skip=skip, limit=limit)


def get_telecom_operator_by_id_service(db: Session, telecom_operator_id: int):
    return get_telecom_operator_by_id(db=db, telecom_operator_id=telecom_operator_id)
