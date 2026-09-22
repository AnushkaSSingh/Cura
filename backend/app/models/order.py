from sqlalchemy import Column, String, Float
from backend.app.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False)
    order_date = Column(String, nullable=True)
    expected_delivery = Column(String, nullable=True)
    actual_delivery = Column(String, nullable=True)
    amount = Column(Float, nullable=True)