from datetime import datetime

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    description: str
    is_active: bool


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True