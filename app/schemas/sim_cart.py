from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseModel


class SimCartBase(BaseModel):
    phone_number: str
    description: Optional[str] = None
    is_active: Optional[bool] = None


class SimCartCreate(SimCartBase):
    telecom_operator_id: int


class SimCartUpdate(SimCartBase):
    is_active: Optional[bool] = None
    telecom_operator_id: Optional[int] = None


class SimCart(SimCartBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
