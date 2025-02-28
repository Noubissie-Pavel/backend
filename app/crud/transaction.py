import logging
import traceback

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreateSchema

logger = logging.getLogger(__name__)


async def create_transaction(db: AsyncSession, transaction_data: TransactionCreateSchema):
    db_transaction = Transaction(**transaction_data.dict())
    db_transaction.status = "PENDING"
    db_transaction.transaction_reference = "TESTING"

    try:
        db.add(db_transaction)
        await db.commit()
        await db.refresh(db_transaction)

        # Load related telecom_operator and operation data
        await db.execute(
            select(Transaction)
            .options(selectinload(Transaction.telecom_operator))
            .options(selectinload(Transaction.operation))
            .filter(Transaction.id == db_transaction.id)
        )

        return db_transaction
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


async def get_transactions(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.telecom_operator))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_transaction_by_id(db: AsyncSession, transaction_id: int):
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    return result.scalars().first()
