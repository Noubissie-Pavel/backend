from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from pydantic import BaseModel

from app.schemas.operationschema import OperationSchema
from app.schemas.sim_cart import SimCartBase


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
    sim_carts: List[SimCartBase]
    operations: List[OperationSchema]
    created_at: datetime
    updated_at: datetime


class TelecomOperatorOneToOne(TelecomOperatorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    operations: List[OperationSchema]


class Config:
    orm_mode = True
