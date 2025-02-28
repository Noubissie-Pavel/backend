from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseModel


class SimCart(BaseModel):
    phone_number: str
    description: Optional[str] = None
    is_active: Optional[bool] = None
    telecom_operator_id: int


class SimCartCreate(SimCart):
    telecom_operator_id: int


class SimCartUpdate(SimCart):
    is_active: Optional[bool] = None
    telecom_operator_id: Optional[int] = None


class SimCart(SimCart):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
