import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.telecom_operator import create_telecom_operator, get_telecom_operators, get_telecom_operator_by_id, \
    update_telecom_operator, delete_telecom_operator
from app.schemas.telecom_operator import TelecomOperatorCreate, TelecomOperatorUpdate

logger = logging.getLogger(__name__)


async def create_telecom_operator_service(db: AsyncSession, telecom_operator: TelecomOperatorCreate):
    try:
        telecom_operator_instance = await create_telecom_operator(db, telecom_operator)
        if telecom_operator_instance is None:
            raise HTTPException(status_code=400,
                                detail=f"Telecom operator with name '{telecom_operator.name}' already exists.")
        return telecom_operator_instance
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_telecom_operator_service: {str(e)}")
        raise


async def get_telecom_operators_service(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await get_telecom_operators(db=db, skip=skip, limit=limit)


async def get_telecom_operator_by_id_service(db: AsyncSession, telecom_operator_id: int):
    telecom_operator = await get_telecom_operator_by_id(db, telecom_operator_id)
    if telecom_operator is None:
        raise HTTPException(status_code=404, detail=f"Telecom operator with id {telecom_operator_id} not found.")
    return telecom_operator


async def update_telecom_operator_service(db: AsyncSession, telecom_operator_id: int,
                                          telecom_operator_data: TelecomOperatorUpdate):
    existing_telecom_operator = await get_telecom_operator_by_id(db, telecom_operator_id)
    if existing_telecom_operator is None:
        raise HTTPException(status_code=404, detail=f"Telecom operator with id {telecom_operator_id} not found.")
    return await update_telecom_operator(db, telecom_operator_id, telecom_operator_data)


async def delete_telecom_operator_service(db: AsyncSession, telecom_operator_id: int):
    existing_telecom_operator = await get_telecom_operator_by_id(db, telecom_operator_id)
    if existing_telecom_operator is None:
        raise HTTPException(status_code=404, detail=f"Telecom operator with id {telecom_operator_id} not found.")
    return await delete_telecom_operator(db, telecom_operator_id)
