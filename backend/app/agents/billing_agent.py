import json
import os
from typing import Dict, Any, List


class BillingAgent:
    """
    Investigates customer payment and billing issues.

    The prototype uses payments.json as the billing data source.
    """

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
        """Load demo payment data."""

        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def find_customer_payments(
        self,
        customer_id: str,
    ) -> List[Dict[str, Any]]:
        """Return all payments belonging to a customer."""

        payments = self._load_payments()

        return [
            payment
            for payment in payments
            if str(payment.get("customer_id")) == str(customer_id)
        ]

    def detect_duplicate_payments(
        self,
        payments: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Detect possible duplicate charges.

        Two payments are considered duplicates when they have
        the same order ID and same amount.
        """

        duplicates = []

        grouped = {}

        for payment in payments:
            key = (
                payment.get("order_id"),
                payment.get("amount"),
            )

            grouped.setdefault(key, []).append(payment)

        for payment_group in grouped.values():
            if len(payment_group) > 1:
                duplicates.extend(payment_group)

        return duplicates

    def investigate(
        self,
        customer_id: str,
        message: str,
    ) -> Dict[str, Any]:
        """Investigate a customer's billing complaint."""

        payments = self.find_customer_payments(customer_id)

        if not payments:
            return {
                "status": "not_found",
                "customer_id": customer_id,
                "message": message,
                "finding": "No payment records were found.",
                "duplicate_charge": False,
                "refund_required": False,
                "action": None,
            }

        duplicates = self.detect_duplicate_payments(payments)

        if duplicates:
            duplicate_amount = duplicates[0].get("amount")

            return {
                "status": "investigated",
                "customer_id": customer_id,
                "duplicate_charge": True,
                "duplicate_count": len(duplicates),
                "duplicate_amount": duplicate_amount,
                "payments": payments,
                "refund_required": True,
                "finding": (
                    f"Possible duplicate payment detected. "
                    f"{len(duplicates)} matching charges were found."
                ),
                "action": "Initiate refund for duplicate charge",
            }

        return {
            "status": "investigated",
            "customer_id": customer_id,
            "duplicate_charge": False,
            "duplicate_count": 0,
            "payments": payments,
            "refund_required": False,
            "finding": "No duplicate payment was detected.",
            "action": "No billing action required",
        }