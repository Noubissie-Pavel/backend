import logging
import traceback

from fastapi import HTTPException
from pygments.lexers import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.operation import Operation
from app.models.telecom_operator import TelecomOperator
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreateSchema
from app.utils.ussd_operations import get_ussd_operation_by_code

logger = logging.getLogger(__name__)


async def create_transaction(db: AsyncSession, transaction_data: TransactionCreateSchema):
    telecom_operator = await db.execute(
        select(TelecomOperator).filter(TelecomOperator.id == transaction_data.telecom_operator_id)
    )
    telecom_operator_result = telecom_operator.scalar_one_or_none()

    if telecom_operator_result is None:
        raise HTTPException(status_code=404,
                            detail=f"TelecomOperator with ID {transaction_data.telecom_operator_id} does not exist.")

    operation = await db.execute(
        select(Operation).filter(Operation.id == transaction_data.operation_id)
    )
    operation_result = operation.scalar_one_or_none()

    if operation_result is None:
        raise HTTPException(status_code=404,
                            detail=f"Operation with ID {transaction_data.operation_id} does not exist.")

    operation_result = get_ussd_operation_by_code(operation_result)

    if operation_result is None:
        raise HTTPException(status_code=404,
                            detail=f"Operation Failed with")
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
        db.add(db_transaction)
        await db.commit()
        await db.refresh(db_transaction)

        result = await db.execute(
            select(Transaction)
            .options(selectinload(Transaction.telecom_operator).selectinload(TelecomOperator.operations))
            .filter(Transaction.id == db_transaction.id)
        )
        return result.scalars().first()

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
    result = await db.execute(
        select(Transaction)
        .options(
            selectinload(Transaction.telecom_operator)
            .selectinload(TelecomOperator.operations)
        )
        .filter(Transaction.id == transaction_id)
    )
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