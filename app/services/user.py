from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.user import create_user, get_users, get_user_by_id, update_user, delete_user
from app.schemas.user import UserCreate, UserUpdate, User


async def create_default_admin(db: AsyncSession):
    user = await get_user_by_id(db, 1)
    if user is None:
        user_data = UserCreate(
            email="admin@admin.com",
            password="admin",
            first_name="Admin",
            last_name="Admin",
            is_active=True
        )
        await create_user(db, user_data)


async def create_user_service(db: AsyncSession, user: UserCreate):
    return await create_user(db, user)


async def get_users_service(db: Session, skip: int = 0, limit: int = 100):
    return await get_users(db, skip, limit)


async def get_user_by_id_service(db: AsyncSession, user_id: int) -> User:
    result = await get_user_by_id(db=db, user_id=user_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return result


async def update_user_service(db: AsyncSession, user_id: int, user_data: UserUpdate) -> User:
    existing_user = await get_user_by_id(db, user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return await update_user(db, user_id, user_data)


async def delete_user_service(db: AsyncSession, user_id: int) -> User:
    existing_user = await get_user_by_id(db, user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return await delete_user(db=db, user_id=user_id)
