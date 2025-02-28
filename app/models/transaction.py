from sqlalchemy import Column, Integer, String, DateTime, func, Boolean

from app.models import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    receiver_phone_number = Column(String, nullable=False, unique=False)
    receiver_name = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    raison = Column(String, nullable=True)
    origin = Column(String, nullable=True)
    transaction_reference = Column(String, nullable=True)
    status = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
