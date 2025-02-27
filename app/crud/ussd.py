from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.ussd import Ussd
from app.schemas.ussd import UssdCreate, UssdUpdate


async def get_ussd(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Ussd).offset(skip).limit(limit))
    return result.scalars().all()


async def create_ussd(db: AsyncSession, ussd_data: UssdCreate):
    db_ussd = Ussd(
        code=ussd_data.code,
        description=ussd_data.description,
        is_active=ussd_data.is_active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    try:
        db.add(db_ussd)
        await db.commit()
        await db.refresh(db_ussd)
        return db_ussd
    except IntegrityError:
        await db.rollback()
        raise ValueError(f"Operator with name {ussd_data.operator_name} already exists.")


async def get_ussd_by_id(db: AsyncSession, ussd_id: int):
    result = await db.execute(select(Ussd).filter(Ussd.id == ussd_id))
    return result.scalars().first()


async def update_ussd(db: AsyncSession, ussd_id: int, ussd_data: UssdUpdate):
    result = await db.execute(select(Ussd).filter(Ussd.id == ussd_id))
    db_ussd = result.scalars().first()
    if db_ussd:
        db_ussd.code = ussd_data.code or db_ussd.code
        db_ussd.description = ussd_data.description or db_ussd.description
        db_ussd.is_active = ussd_data.is_active or db_ussd.is_active
        db_ussd.updated_at = datetime.now()

        try:
            await db.commit()
            await db.refresh(db_ussd)
            return db_ussd
        except IntegrityError:
            await db.rollback()
            raise ValueError(f"Operator with name {ussd_data.operator_name} already exists.")
    return None


async def delete_ussd(db: AsyncSession, ussd_id: int):
    result = await db.execute(select(Ussd).filter(Ussd.id == ussd_id))
    db_ussd = result.scalars().first()
    if db_ussd:
        await db.delete(db_ussd)
        await db.commit()
        return db_ussd
    return None
