from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseModel


class OperationBaseSchema(BaseModel):
    name: str
    description: Optional[str]
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True
        from_attributes = True


class OperationCreateSchema(OperationBaseSchema):
    telecom_operator_id: int
    ussd_code: str


class OperationUpdateSchema(OperationBaseSchema):
    is_active: Optional[bool] = None
    telecom_operator_id: Optional[int] = None
    ussd_code: Optional[str] = None


class OperationSchema(OperationBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
