from sqlalchemy.orm import Session

from app.crud.transaction import create_transaction, get_transactions, get_transaction_by_id
from app.schemas.transaction import TransactionCreate


def create_transaction_service(db: Session, transaction_data: TransactionCreate):
    return create_transaction(db=db, transaction_data=transaction_data)


def get_transactions_service(db: Session, skip: int = 0, limit: int = 100):
    return get_transactions(db=db, skip=skip, limit=limit)


def get_transaction_by_id_service(db: Session, transaction_id: int):
    return get_transaction_by_id(db=db, transaction_id=transaction_id)
