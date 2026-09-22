import json
import os
from typing import Any, Dict, List, Optional


class EscalationService:
    def __init__(self):
        self.data_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "data",
            "tickets.json",
        )

    def _load_tickets(self) -> List[Dict[str, Any]]:
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_customer_escalations(
        self, customer_id: str
    ) -> List[Dict[str, Any]]:
        tickets = self._load_tickets()

        return [
            ticket
            for ticket in tickets
            if str(ticket.get("customer_id")) == str(customer_id)
            and str(ticket.get("status", "")).lower()
            in {"escalated", "escalation"}
        ]

    def create_escalation(
        self,
        customer_id: str,
        reason: str,
        priority: str = "medium",
        ticket_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "customer_id": customer_id,
            "ticket_id": ticket_id,
            "reason": reason,
            "priority": priority,
            "status": "pending_human_review",
        }