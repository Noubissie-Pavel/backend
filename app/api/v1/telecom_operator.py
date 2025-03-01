from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.telecom_operator import TelecomOperatorCreate, TelecomOperator, TelecomOperatorUpdate
from app.services.telocom_operator import create_telecom_operator_service, get_telecom_operators_service, \
    get_telecom_operator_by_id_service, update_telecom_operator_service, delete_telecom_operator_service
from app.utils.utils import PAGE_LIMIT

telecom_operator_v1 = APIRouter()


@telecom_operator_v1.post("/telecom_operator", response_model=TelecomOperator)
async def create_telecom_operator_endpoint(telecom_operator: TelecomOperatorCreate,
                                           db: AsyncSession = Depends(get_db),
                                           request: Request = None):
    try:
        request.state.response_message = 'Telecom Operator created successfully'
        return await create_telecom_operator_service(db, telecom_operator)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@telecom_operator_v1.get("/telecom_operators", response_model=list[TelecomOperator])
async def get_telecom_operators_endpoint(skip: int = 0, limit: int = PAGE_LIMIT,
                                         db: AsyncSession = Depends(get_db),
                                         request: Request = None):
    try:
        request.state.response_message = 'All telecom operators'
        return await get_telecom_operators_service(db, skip, limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@telecom_operator_v1.get("/telecom_operator/{telecom_operator_id}", response_model=TelecomOperator)
async def get_telecom_operator_endpoint(telecom_operator_id: int, db: AsyncSession = Depends(get_db),
                                        request: Request = None):
    try:
        response = await get_telecom_operator_by_id_service(db, telecom_operator_id)
        request.state.response_message = f'Telecom operator with id {telecom_operator_id} fetched successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Telecom operator with id {telecom_operator_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@telecom_operator_v1.put("/telecom_operator/{telecom_operator_id}", response_model=TelecomOperator)
async def update_telecom_operator_endpoint(telecom_operator_id: int, telecom_operator: TelecomOperatorUpdate,
                                           db: AsyncSession = Depends(get_db),
                                           request: Request = None):
    try:
        response = await update_telecom_operator_service(db, telecom_operator_id, telecom_operator)
        request.state.response_message = f'Telecom operator with id {telecom_operator_id} updated successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Telecom operator with id {telecom_operator_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@telecom_operator_v1.delete("/telecom_operator/{telecom_operator_id}", response_model=TelecomOperator)
async def delete_telecom_operator_endpoint(telecom_operator_id: int, db: AsyncSession = Depends(get_db),
                                           request: Request = None):
    try:
        response = await delete_telecom_operator_service(db, telecom_operator_id)
        request.state.response_message = f'Telecom operator with id {telecom_operator_id} deleted successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Telecom operator with id {telecom_operator_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
