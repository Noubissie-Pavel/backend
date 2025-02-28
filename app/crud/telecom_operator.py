import logging
import traceback
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.models.telecom_operator import TelecomOperator
from app.schemas.telecom_operator import TelecomOperatorCreate, TelecomOperatorUpdate

logger = logging.getLogger(__name__)


async def create_telecom_operator(db: AsyncSession, telecom_operator_data: TelecomOperatorCreate):
    db_telecom_operator = TelecomOperator(
        operator_name=telecom_operator_data.operator_name,
        description=telecom_operator_data.description,
        is_active=telecom_operator_data.is_active,
        country=telecom_operator_data.country,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    try:
        db.add(db_telecom_operator)
        await db.commit()
        await db.refresh(db_telecom_operator)

        result = await db.execute(
            select(TelecomOperator)
            .options(selectinload(TelecomOperator.sim_carts))
            .options(selectinload(TelecomOperator.operations))
            .filter(TelecomOperator.id == db_telecom_operator.id)
        )
        return result.scalars().first()
    except IntegrityError as e:
        await db.rollback()
        if "unique constraint" in str(e).lower():
            logger.error(f"Telecom Operator with name {telecom_operator_data.operator_name} already exists.")
            return None
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


async def get_telecom_operators(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(TelecomOperator)
        .options(selectinload(TelecomOperator.sim_carts))
        .options(selectinload(TelecomOperator.operations))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_telecom_operator_by_id(db: AsyncSession, telecom_operator_id: int):
    result = await db.execute(
        select(TelecomOperator)
        .filter(TelecomOperator.id == telecom_operator_id)
        .options(selectinload(TelecomOperator.sim_carts))
    )
    return result.scalars().first()


async def update_telecom_operator(db: AsyncSession, telecom_operator_id: int,
                                  telecom_operator_data: TelecomOperatorUpdate):
    result = await db.execute(select(TelecomOperator).filter(TelecomOperator.id == telecom_operator_id))
    db_telecom_operator = result.scalars().first()
    if db_telecom_operator:
        db_telecom_operator.description = telecom_operator_data.description or db_telecom_operator.description
        db_telecom_operator.operator_name = telecom_operator_data.operator_name or db_telecom_operator.operator_name
        db_telecom_operator.is_active = telecom_operator_data.is_active or db_telecom_operator.is_active
        db_telecom_operator.country = telecom_operator_data.country or db_telecom_operator.country
        db_telecom_operator.updated_at = datetime.now()
        try:
            await db.commit()
            await db.refresh(db_telecom_operator)
            return db_telecom_operator
        except IntegrityError:
            await db.rollback()
            raise ValueError(f"Telecom Operator with name {telecom_operator_data.operator_name} already exists.")
    return None


async def delete_telecom_operator(db: AsyncSession, telecom_operator_id: int):
    result = await db.execute(select(TelecomOperator).filter(TelecomOperator.id == telecom_operator_id))
    db_telecom_operator = result.scalars().first()
    if db_telecom_operator:
        await db.delete(db_telecom_operator)
        await db.commit()
        return db_telecom_operator
    return None
