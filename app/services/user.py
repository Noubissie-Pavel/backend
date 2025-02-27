from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.crud.user import crud_create_user
from app.models.user import User
from app.schemas.user import UserCreate


async def create_default_admin(db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == "admin@example.com"))
    existing_admin = result.scalar_one_or_none()

    if existing_admin:
        return existing_admin

    admin_data = UserCreate(
        email="admin@example.com",
        password="admin",
        first_name="admin",
        last_name="admin",
        is_active=True
    )

    return await crud_create_user(db=db, user=admin_data)

#
# def create_user_service(db: Session, user: UserCreate):
#     return crud_create_user(db=db, user=user)
#
#
# def get_users_service(db: Session, skip: int = 0, limit: int = 100):
#     return crud_get_users(db=db, skip=skip, limit=limit)
