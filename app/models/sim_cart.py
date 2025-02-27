from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SimCart(Base):
    __tablename__ = "sim_cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
