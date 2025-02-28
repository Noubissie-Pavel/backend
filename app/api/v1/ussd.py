from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ussdschema import UssdSchema, UssdCreateSchema
from app.services.ussd import get_ussd_service, create_ussd_service, update_ussd_service, delete_ussd_service, \
    get_ussd_by_id_service
from app.utils.utils import PAGE_LIMIT

ussd_v1 = APIRouter()


@ussd_v1.get("/ussd", response_model=list[UssdSchema])
async def get_ussd_endpoint(
        skip: int = 0,
        limit: int = PAGE_LIMIT,
        db: AsyncSession = Depends(get_db),
        request: Request = None):
    try:
        request.state.response_message = f'All Ussd data. {skip} - {limit}'
        return await get_ussd_service(db, skip, limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ussd_v1.get("/ussd/{ussd_id}", response_model=UssdSchema)
async def get_one_ussd_endpoint(
        ussd_id: int,
        db: AsyncSession = Depends(get_db),
        request: Request = None):
    try:
        response = await get_ussd_by_id_service(db, ussd_id)
        request.state.response_message = f'Ussd with id {ussd_id} fetched successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Ussd with id {ussd_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ussd_v1.post("/ussd", response_model=UssdSchema)
async def create_ussd_endpoint(
        ussd_data: UssdCreateSchema,
        db: AsyncSession = Depends(get_db),
        request: Request = None):
    try:
        request.state.response_message = 'Ussd created successfully'
        return await create_ussd_service(db, ussd_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ussd_v1.put("/ussd/{ussd_id}", response_model=UssdSchema)
async def update_ussd_endpoint(
        ussd_id: int,
        ussd_data: UssdCreateSchema,
        db: AsyncSession = Depends(get_db),
        request: Request = None):
    try:
        response = await update_ussd_service(db, ussd_id, ussd_data)
        request.state.response_message = f'Ussd with id {ussd_id} updated successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Ussd with id {ussd_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ussd_v1.delete("/ussd/{ussd_id}", response_model=UssdSchema)
async def delete_ussd_endpoint(
        ussd_id: int,
        db: AsyncSession = Depends(get_db),
        request: Request = None):
    try:
        response = await delete_ussd_service(db, ussd_id)
        request.state.response_message = f'Ussd with id {ussd_id} deleted successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Ussd with id {ussd_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
