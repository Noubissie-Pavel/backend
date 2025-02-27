from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


def create_transaction(db: Session, transaction_data: TransactionCreate):
    db_transaction = Transaction(
        receiver_phone_number=transaction_data.receiver_phone_number,
        receiver_name=transaction_data.receiver_name,
        amount=transaction_data.amount,
        raison=transaction_data.raison,
        origin=transaction_data.origin,
        transaction_reference='PENDING',
        is_active=transaction_data.is_active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).offset(skip).limit(limit).all()


def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()
