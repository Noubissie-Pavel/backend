from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.telecom_operator import TelecomOperator
from app.schemas.telecom_operator import TelecomOperatorCreate, TelecomOperatorUpdate


def create_telecom_operator(db: Session, telecom_operator: TelecomOperatorCreate):
    db_telecom_operator = TelecomOperator(
        operator_name=telecom_operator.operator_name,
        description=telecom_operator.description,
        is_active=telecom_operator.is_active,
        country=telecom_operator.country,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    try:
        db.add(db_telecom_operator)
        db.commit()
        db.refresh(db_telecom_operator)
        return db_telecom_operator
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Operator with name {telecom_operator.operator_name} already exists.")


def get_telecom_operators(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TelecomOperator).offset(skip).limit(limit).all()


def get_telecom_operator_by_id(db: Session, telecom_operator_id: int):
    return db.query(TelecomOperator).filter(TelecomOperator.id == telecom_operator_id).first()


def update_telecom_operator(db: Session, telecom_operator_id: int, telecom_operator_data: TelecomOperatorUpdate):
    db_telecom_operator = db.query(TelecomOperator).filter(TelecomOperator.id == telecom_operator_id).first()
    if db_telecom_operator:
        db_telecom_operator.description = telecom_operator_data.description or db_telecom_operator.description
        db_telecom_operator.operator_name = telecom_operator_data.operator_name or db_telecom_operator.operator_name
        db_telecom_operator.is_active = telecom_operator_data.is_active or db_telecom_operator.is_active
        db_telecom_operator.country = telecom_operator_data.country or db_telecom_operator.country
        db_telecom_operator.updated_at = datetime.now()

        try:
            db.commit()
            db.refresh(db_telecom_operator)
            return db_telecom_operator
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Operator with name {telecom_operator_data.operator_name} already exists.")
    return None


def delete_telecom_operator(db: Session, telecom_operator_id: int):
    db_telecom_operator = db.query(TelecomOperator).filter(
        TelecomOperator.id == telecom_operator_id).first()
    if db_telecom_operator:
        db.delete(db_telecom_operator)
        db.commit()
        return db_telecom_operator
    return None