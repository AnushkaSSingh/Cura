from pydantic import BaseModel
from typing import Optional


class TicketCreate(BaseModel):
    customer_id: str
    subject: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None


class TicketResponse(TicketCreate):
    ticket_id: str
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True