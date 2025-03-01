from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UssdBase(BaseModel):
    code: str
    description: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True
        from_attributes = True


class UssdCreateSchema(UssdBase):
    pass


class UssdUpdateSchema(UssdBase):
    pass


class UssdSchema(UssdBase):
    id: int
    created_at: datetime
    updated_at: datetime
