from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseModel


class OperationBase(BaseModel):
    name: str
    description: Optional[str]
    is_active: Optional[bool] = None


class OperationCreate(OperationBase):
    pass


class OperationUpdate(OperationBase):
    is_active: Optional[bool] = None


class Operation(OperationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        orm_mode = True
