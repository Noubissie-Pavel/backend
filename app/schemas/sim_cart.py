from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseModel


class SimCartBase(BaseModel):
    phone_number: str
    description: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True
        from_attributes = True


class SimCartCreate(SimCartBase):
    telecom_operator_id: int
    secret_code: str


class SimCartUpdate(SimCartBase):
    is_active: Optional[bool] = None
    telecom_operator_id: Optional[int] = None
    secret_code: Optional[str] = None


class SimCartSchema(SimCartBase):
    id: int
    created_at: datetime
    updated_at: datetime
    secret_code: str
