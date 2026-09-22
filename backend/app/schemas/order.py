from pydantic import BaseModel
from typing import Optional


class OrderResponse(BaseModel):
    order_id: str
    customer_id: str
    status: str
    order_date: Optional[str] = None
    expected_delivery: Optional[str] = None
    actual_delivery: Optional[str] = None
    amount: Optional[float] = None

    class Config:
        from_attributes = True