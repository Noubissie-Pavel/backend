from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.ussd import create_ussd, get_ussd, get_ussd_by_id, update_ussd, delete_ussd
from app.schemas.ussd import UssdCreate, UssdUpdate, Ussd


async def create_ussd_service(db: AsyncSession, ussd_data: UssdCreate):
    return await create_ussd(db, ussd_data)


async def get_ussd_service(db: Session, skip: int = 0, limit: int = 100):
    return await get_ussd(db, skip, limit)


async def get_ussd_by_id_service(db: AsyncSession, ussd_id: int) -> Ussd:
    result = await get_ussd_by_id(db=db, ussd_id=ussd_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Ussd with id {ussd_id} not found.")
    return result


async def update_ussd_service(db: AsyncSession, ussd_id: int, ussd_data: UssdUpdate) -> Ussd:
    existing_ussd = await get_ussd_by_id(db, ussd_id)
    if existing_ussd is None:
        raise HTTPException(status_code=404, detail=f"Ussd with id {ussd_id} not found.")
    return await update_ussd(db, ussd_id, ussd_data)


async def delete_ussd_service(db: AsyncSession, ussd_id: int) -> Ussd:
    existing_ussd = await get_ussd_by_id(db, ussd_id)
    if existing_ussd is None:
        raise HTTPException(status_code=404, detail=f"Ussd with id {ussd_id} not found.")
    return await delete_ussd(db=db, ussd_id=ussd_id)
