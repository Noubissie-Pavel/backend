from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseModel


class SimCart(BaseModel):
    phone_number: str
    description: Optional[str] = None
    is_active: Optional[bool] = None


class SimCartCreate(SimCart):
    pass


class SimCartUpdate(SimCart):
    is_active: Optional[bool] = None


class SimCart(SimCart):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
