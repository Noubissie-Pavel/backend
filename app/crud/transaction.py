import logging
import traceback

from pygments.lexers import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.telecom_operator import TelecomOperator
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreateSchema

logger = logging.getLogger(__name__)


async def create_transaction(db: AsyncSession, transaction_data: TransactionCreateSchema):
    db_transaction = Transaction(
        receiver_phone_number=transaction_data.receiver_phone_number,
        receiver_name=transaction_data.receiver_name,
        amount=transaction_data.amount,
        raison=transaction_data.raison,
        origin=transaction_data.origin,
        telecom_operator_id=transaction_data.telecom_operator_id,
        operation_id=transaction_data.operation_id,
        status="PENDING",
        transaction_reference="TESTING"
    )

    try:
        # Add the transaction to the session and commit it asynchronously
        db.add(db_transaction)
        await db.commit()
        await db.refresh(db_transaction)  # Ensure refreshing the db_transaction to get latest data

        # Fetch the transaction with related telecom_operator and operations asynchronously
        result = await db.execute(
            select(Transaction)
            .options(selectinload(Transaction.telecom_operator).selectinload(TelecomOperator.operations))
            .filter(Transaction.id == db_transaction.id)
        )

        return result.scalars().first()  # Return the created transaction with related data
    except IntegrityError as e:
        await db.rollback()
        if "unique constraint" in str(e).lower():
            logger.error(f"Transaction with reference {transaction_data.transaction_reference} already exists.")
            return None
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


async def get_transaction_by_id(db: AsyncSession, transaction_id: int):
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    return result.scalars().first()


async def get_transactions(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Transaction)
        .options(
            selectinload(Transaction.telecom_operator)
            .selectinload(TelecomOperator.operations)
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
