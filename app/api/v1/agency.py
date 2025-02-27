from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.agency import AgencyCreate, Agency
from app.services.agency import create_agency_service, get_agencies_service, get_agency_by_id_service, \
    update_agency_service, delete_agency_service
from app.utils.utils import PAGE_LIMIT

agency_v1 = APIRouter()


@agency_v1.post("/agency", response_model=Agency)
async def create_agency_endpoint(agency: AgencyCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_agency_service(db, agency)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@agency_v1.get("/agencies", response_model=list[Agency])
async def get_agencies_endpoint(skip: int = 0, limit: int = PAGE_LIMIT, db: AsyncSession = Depends(get_db),
                                request: Request = None):
    try:
        request.state.response_message = f'All agencies. {skip} - {skip + limit}'
        return await get_agencies_service(db, skip, limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@agency_v1.get("/agency/{agency_id}", response_model=Agency)
async def get_one_agency_endpoint(agency_id: int, db: AsyncSession = Depends(get_db), request: Request = None):
    try:
        response = await get_agency_by_id_service(db, agency_id)
        request.state.response_message = f'Agency with id {agency_id} fetched successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Agency with id {agency_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@agency_v1.put("/agency/{agency_id}", response_model=Agency)
async def update_agency_endpoint(agency_id: int, agency: AgencyCreate, db: AsyncSession = Depends(get_db),
                                 request: Request = None):
    try:
        response = await update_agency_service(db, agency_id, agency)
        request.state.response_message = f'Agency with id {agency_id} updated successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Agency with id {agency_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@agency_v1.delete("/agency/{agency_id}", response_model=Agency)
async def delete_agency_endpoint(agency_id: int, db: AsyncSession = Depends(get_db), request: Request = None):
    try:
        response = await delete_agency_service(db, agency_id)
        request.state.response_message = f'Agency with id {agency_id} deleted successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Agency with id {agency_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
