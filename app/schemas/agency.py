from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AgencyBase(BaseModel):
    name: str
    agency_code: str
    description: Optional[str] = None
    address: str
    is_active: Optional[bool] = None


class AgencyCreate(AgencyBase):
    pass


class AgencyUpdate(AgencyBase):
    pass


class Agency(AgencyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
