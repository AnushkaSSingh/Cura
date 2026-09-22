import json
import os
from typing import Dict, Any, Optional


class OrderAgent:
    """
    Investigates customer order and delivery issues.

    The prototype reads order information from the local JSON
    demo data instead of requiring a real e-commerce database.
    """

    def __init__(self):
        self.data_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "data",
            "orders.json",
        )

    def _load_orders(self):
        """Load demo order data."""

        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def find_customer_orders(
        self,
        customer_id: str,
    ):
        """Return all orders belonging to a customer."""

        orders = self._load_orders()

        return [
            order
            for order in orders
            if str(order.get("customer_id")) == str(customer_id)
        ]

    def find_relevant_order(
        self,
        customer_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Find the most relevant order.

        For the prototype, the latest order is treated as the
        relevant order.
        """

        orders = self.find_customer_orders(customer_id)

        if not orders:
            return None

        return orders[-1]

    def investigate(
        self,
        customer_id: str,
        message: str,
    ) -> Dict[str, Any]:
        """
        Investigate an order-related customer complaint.
        """

        order = self.find_relevant_order(customer_id)

        if not order:
            return {
                "status": "not_found",
                "customer_id": customer_id,
                "message": message,
                "finding": "No order was found for this customer.",
                "action": None,
            }

        status = str(order.get("status", "")).lower()

        delayed_statuses = [
            "delayed",
            "late",
            "processing",
            "shipped",
        ]

        is_delayed = status in delayed_statuses

        if is_delayed:
            finding = (
                f"Order {order.get('order_id')} is currently "
                f"marked as {order.get('status')}."
            )
        else:
            finding = (
                f"Order {order.get('order_id')} was found with "
                f"status {order.get('status')}."
            )

        return {
            "status": "investigated",
            "customer_id": customer_id,
            "order_id": order.get("order_id"),
            "order_status": order.get("status"),
            "order_date": order.get("order_date"),
            "expected_delivery": order.get("expected_delivery"),
            "actual_delivery": order.get("actual_delivery"),
            "amount": order.get("amount"),
            "is_delayed": is_delayed,
            "finding": finding,
            "action": (
                "Investigate delivery delay"
                if is_delayed
                else "No delivery action required"
            ),
        }