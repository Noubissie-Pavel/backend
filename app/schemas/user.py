from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    is_active: bool


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
