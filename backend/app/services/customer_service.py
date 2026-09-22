import json
import os
from typing import Any, Dict, List, Optional


class CustomerService:
    def __init__(self):
        self.data_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "data",
            "customers.json",
        )

    def _load_customers(self) -> List[Dict[str, Any]]:
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_all_customers(self) -> List[Dict[str, Any]]:
        return self._load_customers()

    def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        customers = self._load_customers()

        for customer in customers:
            if str(customer.get("customer_id")) == str(customer_id):
                return customer

        return None