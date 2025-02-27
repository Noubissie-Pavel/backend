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



class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    is_active: Optional[bool] = None
    status: Optional[str] = None


class Transaction(TransactionBase):
    id: int
    transaction_reference: str
    created_at: datetime
    updated_at: datetime
    is_active: Optional[bool] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True
