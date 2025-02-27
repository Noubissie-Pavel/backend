import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.sim_cart import create_sim_cart, get_sim_carts, get_sim_cart_by_id, update_sim_cart, delete_sim_cart
from app.schemas.sim_cart import SimCartCreate, SimCartUpdate

logger = logging.getLogger(__name__)


async def create_sim_cart_service(db: AsyncSession, sim_cart_data: SimCartCreate):
    try:
        sim_cart_instance = await create_sim_cart(db, sim_cart_data)
        if sim_cart_instance is None:
            raise HTTPException(status_code=400,
                                detail=f"Sim cart with phone number '{sim_cart_data.phone_number}' already exists.")
        return sim_cart_instance
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_sim_cart_service: {str(e)}")
        raise


async def get_sim_carts_service(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await get_sim_carts(db=db, skip=skip, limit=limit)


async def get_sim_cart_by_id_service(db: AsyncSession, sim_cart_id: int):
    sim_cart = await get_sim_cart_by_id(db, sim_cart_id)
    if sim_cart is None:
        raise HTTPException(status_code=404, detail=f"Sim cart with id {sim_cart_id} not found.")
    return sim_cart


async def update_sim_cart_service(db: AsyncSession, sim_cart_id: int, sim_cart_data: SimCartUpdate):
    existing_sim_cart = await get_sim_cart_by_id(db, sim_cart_id)
    if existing_sim_cart is None:
        raise HTTPException(status_code=404, detail=f"Sim cart with id {sim_cart_id} not found.")
    return await update_sim_cart(db, sim_cart_id, sim_cart_data)


async def delete_sim_cart_service(db: AsyncSession, sim_cart_id: int):
    existing_sim_cart = await get_sim_cart_by_id(db, sim_cart_id)
    if existing_sim_cart is None:
        raise HTTPException(status_code=404, detail=f"Sim cart with id {sim_cart_id} not found.")
    return await delete_sim_cart(db, sim_cart_id)
