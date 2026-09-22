import json
import os
from typing import Any, Dict, List, Optional


class TicketService:
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

    def get_all_tickets(self) -> List[Dict[str, Any]]:
        return self._load_tickets()

    def get_customer_tickets(
        self, customer_id: str
    ) -> List[Dict[str, Any]]:
        tickets = self._load_tickets()

        return [
            ticket
            for ticket in tickets
            if str(ticket.get("customer_id")) == str(customer_id)
        ]

    def get_ticket(
        self, ticket_id: str
    ) -> Optional[Dict[str, Any]]:
        tickets = self._load_tickets()

        for ticket in tickets:
            if str(ticket.get("ticket_id")) == str(ticket_id):
                return ticket

        return None

    def get_open_tickets(
        self, customer_id: str
    ) -> List[Dict[str, Any]]:
        tickets = self.get_customer_tickets(customer_id)

        return [
            ticket
            for ticket in tickets
            if str(ticket.get("status", "")).lower()
            in {"open", "pending", "in_progress"}
        ]