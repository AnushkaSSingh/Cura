from typing import Dict, Any


class SupportPolicy:
    """
    Centralized rules that determine which support actions
    Cura is allowed to perform automatically.
    """

    def __init__(self):
        self.rules = {
            "duplicate_payment_refund": {
                "allowed": True,
                "requires_human": False,
            },
            "order_delay_investigation": {
                "allowed": True,
                "requires_human": False,
            },
            "unknown_issue": {
                "allowed": False,
                "requires_human": True,
            },
        }

    def can_execute(
        self,
        action: str,
    ) -> bool:
        """Check whether an action is permitted."""

        rule = self.rules.get(action)

        if not rule:
            return False

        return (
            rule["allowed"]
            and not rule["requires_human"]
        )

    def get_rule(
        self,
        action: str,
    ) -> Dict[str, Any]:
        """Return the policy associated with an action."""

        return self.rules.get(
            action,
            {
                "allowed": False,
                "requires_human": True,
            },
        )

    def evaluate_action(
        self,
        action: str,
    ) -> Dict[str, Any]:
        """Return a structured policy decision."""

        rule = self.get_rule(action)

        if rule["allowed"] and not rule["requires_human"]:
            return {
                "action": action,
                "allowed": True,
                "decision": "AUTO_EXECUTE",
                "reason": "Action is permitted by support policy.",
            }

        return {
            "action": action,
            "allowed": False,
            "decision": "HUMAN_REVIEW",
            "reason": "Action requires human review or is not permitted.",
        }