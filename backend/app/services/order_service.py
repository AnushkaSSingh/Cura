import json
import os
from typing import Any, Dict, List, Optional


class OrderService:
    def __init__(self):
        self.data_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "data",
            "orders.json",
        )

    def _load_orders(self) -> List[Dict[str, Any]]:
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_all_orders(self) -> List[Dict[str, Any]]:
        return self._load_orders()

    def get_customer_orders(self, customer_id: str) -> List[Dict[str, Any]]:
        orders = self._load_orders()

        return [
            order
            for order in orders
            if str(order.get("customer_id")) == str(customer_id)
        ]

    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        orders = self._load_orders()

        for order in orders:
            if str(order.get("order_id")) == str(order_id):
                return order

        return None

    def get_latest_customer_order(
        self, customer_id: str
    ) -> Optional[Dict[str, Any]]:
        orders = self.get_customer_orders(customer_id)

        if not orders:
            return None

        return orders[-1]