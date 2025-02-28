from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models import Base  # Assuming you have a shared Base object


class SimCart(Base):
    __tablename__ = "sim_cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    telecom_operator_id = Column(Integer, ForeignKey('telecom_operator.id'))

    telecom_operator = relationship("TelecomOperator", back_populates="sim_carts")
