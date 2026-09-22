from pydantic import BaseModel
from typing import Optional


class EscalationCreate(BaseModel):
    customer_id: str
    ticket_id: Optional[str] = None
    reason: str
    priority: Optional[str] = None


class EscalationResponse(EscalationCreate):
    escalation_id: str
    status: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True