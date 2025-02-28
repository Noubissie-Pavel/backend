from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseModel


class TransactionBase(BaseModel):
    receiver_phone_number: str
    receiver_name: str
    amount: int
    raison: str
    origin: str
    is_active: Optional[bool] = None


class TransactionCreateSchema(TransactionBase):
    telecom_operator_id: int
    operation_id: int


class TransactionUpdateSchema(TransactionBase):
    is_active: Optional[bool] = None
    status: Optional[str] = None


class TransactionSchema(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    telecom_operator_id: int
    operation_id: int
    transaction_reference: str
    is_active: Optional[bool] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True
