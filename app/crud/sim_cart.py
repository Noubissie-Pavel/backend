import logging
import traceback
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.sim_cart import SimCart
from app.schemas.sim_cart import SimCartCreate, SimCartUpdate

logger = logging.getLogger(__name__)


async def create_sim_cart(db: AsyncSession, sim_cart_data: SimCartCreate):
    db_sim_cart = SimCart(
        phone_number=sim_cart_data.phone_number,
        description=sim_cart_data.description,
        is_active=sim_cart_data.is_active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    try:
        db.add(db_sim_cart)
        await db.commit()
        await db.refresh(db_sim_cart)
        return db_sim_cart
    except IntegrityError as e:
        await db.rollback()
        if "unique constraint" in str(e).lower():
            logger.error(f"Sim Cart with phone number {sim_cart_data.phone_number} already exists.")
            return None
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


async def get_sim_carts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(SimCart).offset(skip).limit(limit))
    return result.scalars().all()


async def get_sim_cart_by_id(db: AsyncSession, sim_cart_id: int):
    result = await db.execute(select(SimCart).filter(SimCart.id == sim_cart_id))
    return result.scalars().first()


async def update_sim_cart(db: AsyncSession, sim_cart_id: int, sim_cart_data: SimCartUpdate):
    result = await db.execute(select(SimCart).filter(SimCart.id == sim_cart_id))
    db_sim_cart = result.scalars().first()
    if db_sim_cart:
        db_sim_cart.phone_number = sim_cart_data.phone_number or db_sim_cart.phone_number
        db_sim_cart.description = sim_cart_data.description or db_sim_cart.description
        db_sim_cart.is_active = sim_cart_data.is_active or db_sim_cart.is_active
        db_sim_cart.updated_at = datetime.now()
        try:
            await db.commit()
            await db.refresh(db_sim_cart)
            return db_sim_cart
        except IntegrityError:
            await db.rollback()
            raise ValueError(f"Sim Cart with phone number {sim_cart_data.phone_number} already exists.")
    return None


async def delete_sim_cart(db: AsyncSession, sim_cart_id: int):
    result = await db.execute(select(SimCart).filter(SimCart.id == sim_cart_id))
    db_sim_cart = result.scalars().first()
    if db_sim_cart:
        await db.delete(db_sim_cart)
        await db.commit()
        return db_sim_cart
    return None
