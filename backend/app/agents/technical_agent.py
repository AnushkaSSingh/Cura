from typing import Dict, Any


class TechnicalAgent:
    """
    Handles technical and product-related customer issues.

    This agent is currently independent from the main prototype
    and can be connected to the orchestrator later.
    """

    def investigate(
        self,
        customer_id: str,
        message: str,
    ) -> Dict[str, Any]:
        message_lower = message.lower()

        technical_keywords = [
            "not working",
            "error",
            "bug",
            "crash",
            "login",
            "website",
            "app",
            "technical",
            "password",
        ]

        detected = any(
            keyword in message_lower
            for keyword in technical_keywords
        )

        if not detected:
            return {
                "status": "not_relevant",
                "customer_id": customer_id,
                "finding": "No technical issue detected.",
                "action": None,
            }

        return {
            "status": "investigated",
            "customer_id": customer_id,
            "issue_type": "technical",
            "finding": "A possible technical issue was detected.",
            "action": "Review technical troubleshooting steps.",
            "requires_human": False,
        }