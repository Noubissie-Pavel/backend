from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from pydantic import BaseModel

from app.schemas.operation import Operation
from app.schemas.sim_cart import SimCart


class TelecomOperatorBase(BaseModel):
    operator_name: str
    description: Optional[str] = None
    is_active: Optional[bool] = None
    country: Optional[str] = None


class TelecomOperatorCreate(TelecomOperatorBase):
    pass


class TelecomOperatorUpdate(TelecomOperatorBase):
    is_active: Optional[bool] = None


class TelecomOperator(TelecomOperatorBase):
    id: int
    sim_carts: List[SimCart]
    operations: List[Operation]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
