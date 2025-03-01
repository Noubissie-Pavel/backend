from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    description: str
    address: str
    is_active: Optional[bool] = None
    class Config:
        orm_mode = True
        from_attributes = True

class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
