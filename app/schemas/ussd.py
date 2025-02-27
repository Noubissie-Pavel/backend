from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UssdBase(BaseModel):
    code: str
    description: Optional[str] = None
    is_active: Optional[bool] = None


class UssdCreate(UssdBase):
    pass


class UssdUpdate(UssdBase):
    pass


class Ussd(UssdBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
