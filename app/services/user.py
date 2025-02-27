from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from app.controller.user import create_user as crud_create_user
from app.controller.user import get_users as crud_get_users
from app.models.user import User
from app.schemas.user import UserCreate


def create_default_admin(db: Session):
    existing_admin = db.query(User).filter(User.email == "admin@example.com").first()

    if existing_admin:
        return existing_admin

    admin_data = UserCreate(
        email="admin@example.com",
        password="admin",
        first_name="admin",
        last_name="admin",
        is_active=True
    )
    return crud_create_user(db=db, user=admin_data)


def create_user_service(db: Session, user: UserCreate):
    return crud_create_user(db=db, user=user)


def get_users_service(db: Session, skip: int = 0, limit: int = 100):
    return crud_get_users(db=db, skip=skip, limit=limit)
