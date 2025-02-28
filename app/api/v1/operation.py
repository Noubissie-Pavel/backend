from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.operationschema import OperationSchema, OperationCreateSchema
from app.services.operation import get_operations_service, create_operation_service, update_operation_service, \
    delete_operation_service, \
    get_operation_by_id_service
from app.utils.utils import PAGE_LIMIT

operation_v1 = APIRouter()


@operation_v1.get("/operations", response_model=list[OperationSchema])
async def get_operations_endpoint(
        skip: int = 0,
        limit: int = PAGE_LIMIT,
        db: AsyncSession = Depends(get_db),
        request: Request = None):
    try:
        request.state.response_message = f'All operation data. {skip} - {limit}'
        return await get_operations_service(db, skip, limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@operation_v1.get("/operation/{operation_id}", response_model=OperationSchema)
async def get_one_operation_endpoint(
        operation_id: int,
        db: AsyncSession = Depends(get_db),
        request: Request = None):
    try:
        response = await get_operation_by_id_service(db, operation_id)
        request.state.response_message = f'Operation with id {operation_id} fetched successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Operation with id {operation_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@operation_v1.post("/operation", response_model=OperationSchema)
async def create_operation_endpoint(
        operation_data: OperationCreateSchema,
        db: AsyncSession = Depends(get_db),
        request: Request = None):
    try:
        request.state.response_message = 'Operation created successfully'
        return await create_operation_service(db, operation_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@operation_v1.put("/operation/{operation_id}", response_model=OperationSchema)
async def update_operation_endpoint(
        operation_id: int,
        operation_data: OperationCreateSchema,
        db: AsyncSession = Depends(get_db),
        request: Request = None):
    try:
        response = await update_operation_service(db, operation_id, operation_data)
        request.state.response_message = f'Operation with id {operation_id} updated successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Operation with id {operation_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@operation_v1.delete("/operation/{operation_id}", response_model=OperationSchema)
async def delete_operation_endpoint(
        operation_id: int,
        db: AsyncSession = Depends(get_db),
        request: Request = None):
    try:
        response = await delete_operation_service(db, operation_id)
        request.state.response_message = f'Operation with id {operation_id} deleted successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Operation with id {operation_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
