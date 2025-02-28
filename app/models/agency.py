from sqlalchemy import Column, Integer, String, DateTime, func, Boolean

from app.models import Base


class Agency(Base):
    __tablename__ = "agency"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    agency_code = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    address = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
