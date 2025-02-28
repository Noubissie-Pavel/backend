from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Operation(Base):
    __tablename__ = "operation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    telecom_operator_id = Column(Integer, ForeignKey('telecom_operator.id'))

    telecom_operator = relationship("TelecomOperator", back_populates="operations")
