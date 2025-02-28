import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.transaction import create_transaction, get_transactions, get_transaction_by_id
from app.schemas.transaction import TransactionCreateSchema

logger = logging.getLogger(__name__)


async def create_transaction_service(db: AsyncSession, transaction_data: TransactionCreateSchema):
    try:
        transaction_instance = await create_transaction(db, transaction_data)
        if transaction_instance is None:
            raise HTTPException(status_code=400,
                                detail=f"Transaction with id '{transaction_data.id}' already exists.")
        return transaction_instance
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_transaction_service: {str(e)}")
        raise


async def get_transactions_service(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await get_transactions(db=db, skip=skip, limit=limit)


async def get_transaction_by_id_service(db: AsyncSession, transaction_id: int):
    transaction = await get_transaction_by_id(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail=f"Transaction with id {transaction_id} not found.")
    return transaction
