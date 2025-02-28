from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.operation import Operation
from app.schemas.operation import OperationCreate, OperationUpdate


async def get_operations(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Operation).offset(skip).limit(limit))
    return result.scalars().all()


async def create_operation(db: AsyncSession, operation_data: OperationCreate):
    db_operation = Operation(
        name=operation_data.name,
        description=operation_data.description,
        is_active=operation_data.is_active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    try:
        db.add(db_operation)
        await db.commit()
        await db.refresh(db_operation)
        return db_operation
    except IntegrityError:
        await db.rollback()
        raise ValueError(f"Operation with name {operation_data.operator_name} already exists.")


async def get_operation_by_id(db: AsyncSession, operation_id: int):
    result = await db.execute(select(Operation).filter(Operation.id == operation_id))
    return result.scalars().first()


async def update_operation(db: AsyncSession, operation_id: int, operation_data: OperationUpdate):
    result = await db.execute(select(Operation).filter(Operation.id == operation_id))
    db_operation = result.scalars().first()
    if db_operation:
        db_operation.name = operation_data.name or db_operation.name
        db_operation.description = operation_data.description or db_operation.description
        db_operation.is_active = operation_data.is_active or db_operation.is_active
        db_operation.updated_at = datetime.now()

        try:
            await db.commit()
            await db.refresh(db_operation)
            return db_operation
        except IntegrityError:
            await db.rollback()
            raise ValueError(f"Operation with name {operation_data.operator_name} already exists.")
    return None


async def delete_operation(db: AsyncSession, operation_id: int):
    result = await db.execute(select(Operation).filter(Operation.id == operation_id))
    db_operation = result.scalars().first()
    if db_operation:
        await db.delete(db_operation)
        await db.commit()
        return db_operation
    return None
