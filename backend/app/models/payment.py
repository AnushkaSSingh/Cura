from sqlalchemy import Column, String, Float
from backend.app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, nullable=False, index=True)
    order_id = Column(String, nullable=True, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=True)
    payment_date = Column(String, nullable=True)