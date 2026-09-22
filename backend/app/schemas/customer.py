from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerResponse(CustomerBase):
    customer_id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True