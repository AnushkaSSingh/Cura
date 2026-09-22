from typing import Dict, Any


class AccountAgent:
    """
    Handles customer account-related support issues.

    This agent is independent and can be connected to the
    orchestrator when account workflows are added.
    """

    def investigate(
        self,
        customer_id: str,
        message: str,
    ) -> Dict[str, Any]:
        message_lower = message.lower()

        account_keywords = [
            "account",
            "profile",
            "email",
            "phone number",
            "address",
            "password",
            "change my details",
            "account access",
        ]

        detected = any(
            keyword in message_lower
            for keyword in account_keywords
        )

        if not detected:
            return {
                "status": "not_relevant",
                "customer_id": customer_id,
                "finding": "No account issue detected.",
                "action": None,
            }

        return {
            "status": "investigated",
            "customer_id": customer_id,
            "issue_type": "account",
            "finding": "A possible account-related issue was detected.",
            "action": "Review customer account information.",
            "requires_human": False,
        }