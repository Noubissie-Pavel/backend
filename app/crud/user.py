from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


async def crud_create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        email=user.email,
        password=user.password,  # make sure to hash passwords in production
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
    )
    db.add(db_user)
    await db.commit()  # Commit asynchronously
    await db.refresh(db_user)  # Refresh asynchronously
    return db_user

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(User).offset(skip).limit(limit).all()
#
#
# def get_user_by_id(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()
#
#
# def update_user(db: Session, user_id: int, user_data: UserUpdate):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if db_user:
#         db_user.email = user_data.email or db_user.email
#         db_user.password = user_data.password or db_user.password
#         db_user.first_name = user_data.first_name or db_user.first_name
#         db_user.last_name = user_data.last_name or db_user.last_name
#         db_user.is_active = user_data.is_active if user_data.is_active is not None else db_user.is_active
#         db_user.updated_at = datetime.now()
#
#         try:
#             db.commit()
#             db.refresh(db_user)
#             return db_user
#         except IntegrityError:
#             db.rollback()
#             raise Exception(f"User with email {user_data.email} already exists.")
#     return None
#
#
# def delete_user(db: Session, user_id: int):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if db_user:
#         db.delete(db_user)
#         db.commit()
#         return db_user
#     return None
