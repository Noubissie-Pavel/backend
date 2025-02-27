from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.sim_cart import SimCartCreate, SimCart, SimCartUpdate
from app.services.sim_cart import create_sim_cart_service, get_sim_carts_service, get_sim_cart_by_id_service, \
    update_sim_cart_service, delete_sim_cart_service
from app.utils.utils import PAGE_LIMIT

sim_cart_v1 = APIRouter()


@sim_cart_v1.post("/sim_cart", response_model=SimCart, )
async def create_sim_cart_endpoint(sim_cart: SimCartCreate, db: AsyncSession = Depends(get_db),
                                   request: Request = None):
    try:
        request.state.response_message = f'Sim cart with phone number {sim_cart.phone_number} created successfully'
        return await create_sim_cart_service(db, sim_cart)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@sim_cart_v1.get("/sim_carts", response_model=list[SimCart])
async def get_sim_carts_endpoint(skip: int = 0, limit: int = PAGE_LIMIT, db: AsyncSession = Depends(get_db),
                                 request: Request = None):
    try:
        request.state.response_message = f'All sim carts. {skip} - {skip + limit}'
        return await get_sim_carts_service(db, skip, limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@sim_cart_v1.get("/sim_cart/{sim_cart_id}", response_model=SimCart)
async def get_one_sim_cart_endpoint(sim_cart_id: int, db: AsyncSession = Depends(get_db), request: Request = None):
    try:
        response = await get_sim_cart_by_id_service(db, sim_cart_id)
        request.state.response_message = f'Sim cart with id {sim_cart_id} fetched successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Sim cart with id {sim_cart_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@sim_cart_v1.put("/sim_cart/{sim_cart_id}", response_model=SimCart)
async def update_sim_cart_endpoint(sim_cart_id: int, sim_cart: SimCartUpdate, db: AsyncSession = Depends(get_db),
                                   request: Request = None):
    try:
        response = await update_sim_cart_service(db, sim_cart_id, sim_cart)
        request.state.response_message = f'Sim cart with id {sim_cart_id} updated successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Sim cart with id {sim_cart_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@sim_cart_v1.delete("/sim_cart/{sim_cart_id}", response_model=SimCart)
async def delete_sim_cart_endpoint(sim_cart_id: int, db: AsyncSession = Depends(get_db), request: Request = None):
    try:
        response = await delete_sim_cart_service(db, sim_cart_id)
        request.state.response_message = f'Sim cart with id {sim_cart_id} deleted successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"Sim cart with id {sim_cart_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
