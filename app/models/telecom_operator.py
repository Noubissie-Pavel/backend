from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.models import Base


class TelecomOperator(Base):
    __tablename__ = "telecom_operator"

    id = Column(Integer, primary_key=True, autoincrement=True)
    operator_name = Column(String, nullable=False, unique=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True, default=True)
    country = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    sim_carts = relationship("SimCart", back_populates="telecom_operator")

    operations = relationship("Operation", back_populates="telecom_operator")

    transactions = relationship("Transaction", back_populates="telecom_operator")
