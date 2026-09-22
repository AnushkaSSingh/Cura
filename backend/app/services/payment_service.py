import json
import os
from typing import Any, Dict, List, Optional


class PaymentService:
    def __init__(self):
        self.data_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "data",
            "payments.json",
        )

    def _load_payments(self) -> List[Dict[str, Any]]:
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_all_payments(self) -> List[Dict[str, Any]]:
        return self._load_payments()

    def get_customer_payments(
        self, customer_id: str
    ) -> List[Dict[str, Any]]:
        payments = self._load_payments()

        return [
            payment
            for payment in payments
            if str(payment.get("customer_id")) == str(customer_id)
        ]

    def get_payment(
        self, payment_id: str
    ) -> Optional[Dict[str, Any]]:
        payments = self._load_payments()

        for payment in payments:
            if str(payment.get("payment_id")) == str(payment_id):
                return payment

        return None

    def find_duplicate_payments(
        self, customer_id: str
    ) -> List[Dict[str, Any]]:
        payments = self.get_customer_payments(customer_id)

        grouped = {}

        for payment in payments:
            key = (
                payment.get("order_id"),
                payment.get("amount"),
            )

            grouped.setdefault(key, []).append(payment)

        duplicates = []

        for payment_group in grouped.values():
            if len(payment_group) > 1:
                duplicates.extend(payment_group)

        return duplicates