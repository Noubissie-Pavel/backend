from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.company import CompanyCreate, Company
from app.services.company import create_company_service, get_companies_service, get_company_by_id_service, \
    update_company_service, delete_company_service
from app.utils.utils import PAGE_LIMIT

company_v1 = APIRouter()


@company_v1.post("/company", response_model=Company)
async def create_company_endpoint(company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_company_service(db, company)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@company_v1.get("/companies", response_model=list[Company])
async def get_companies_endpoint(skip: int = 0, limit: int = PAGE_LIMIT, db: AsyncSession = Depends(get_db),
                                 request: Request = None):
    try:
        request.state.response_message = f'All companies. {skip} - {skip + limit}'
        return await get_companies_service(db, skip, limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@company_v1.get("/company/{company_id}", response_model=Company)
async def get_one_company_endpoint(company_id: int, db: AsyncSession = Depends(get_db), request: Request = None):
    try:
        response = await get_company_by_id_service(db, company_id)
        request.state.response_message = f'Company with id {company_id} fetched successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Company with id {company_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@company_v1.put("/company/{company_id}", response_model=Company)
async def update_company_endpoint(company_id: int, company: CompanyCreate, db: AsyncSession = Depends(get_db),
                                  request: Request = None):
    try:
        response = await update_company_service(db, company_id, company)
        request.state.response_message = f'Company with id {company_id} updated successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Company with id {company_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@company_v1.delete("/company/{company_id}", response_model=Company)
async def delete_company_endpoint(company_id: int, db: AsyncSession = Depends(get_db), request: Request = None):
    try:
        response = await delete_company_service(db, company_id)
        request.state.response_message = f'Company with id {company_id} deleted successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Company with id {company_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
