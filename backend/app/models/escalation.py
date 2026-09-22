from sqlalchemy import Column, String, Text
from backend.app.database import Base


class Escalation(Base):
    __tablename__ = "escalations"

    escalation_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, nullable=False, index=True)
    ticket_id = Column(String, nullable=True)
    reason = Column(Text, nullable=False)
    status = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    created_at = Column(String, nullable=True)