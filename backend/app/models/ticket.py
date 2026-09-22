from sqlalchemy import Column, String, Text
from backend.app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    created_at = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)