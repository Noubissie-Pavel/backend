from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.operation import create_operation, get_operations, get_operation_by_id, update_operation, delete_operation
from app.schemas.operationschema import OperationCreateSchema, OperationUpdateSchema, OperationSchema


async def create_operation_service(db: AsyncSession, operation_data: OperationCreateSchema):
    return await create_operation(db, operation_data)


async def get_operations_service(db: Session, skip: int = 0, limit: int = 100):
    return await get_operations(db, skip, limit)


async def get_operation_by_id_service(db: AsyncSession, operation_id: int) -> OperationSchema:
    result = await get_operation_by_id(db=db, operation_id=operation_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Operation with id {operation_id} not found.")
    return result


async def update_operation_service(db: AsyncSession, operation_id: int, operation_data: OperationUpdateSchema) -> OperationSchema:
    existing_operation = await get_operation_by_id(db, operation_id)
    if existing_operation is None:
        raise HTTPException(status_code=404, detail=f"Operation with id {operation_id} not found.")
    return await update_operation(db, operation_id, operation_data)


async def delete_operation_service(db: AsyncSession, operation_id: int) -> OperationSchema:
    existing_operation = await get_operation_by_id(db, operation_id)
    if existing_operation is None:
        raise HTTPException(status_code=404, detail=f"Operation with id {operation_id} not found.")
    return await delete_operation(db=db, operation_id=operation_id)
