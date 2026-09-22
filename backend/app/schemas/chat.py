from typing import Any, Dict, Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    customer_id: str
    message: str


class ChatResponse(BaseModel):
    customer_id: str
    message: str
    intent: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    escalated: bool = False