from typing import Dict, Any


class EscalationAgent:
    """
    Determines whether Cura can handle a support case automatically
    or whether it should be escalated to a human support agent.
    """

    def evaluate(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Evaluate the complete investigation and produce a
        resolve/escalate decision with reasoning.
        """

        order = investigation.get("order")
        billing = investigation.get("billing")

        reasons = []
        actions = []

        # Check order investigation
        if order:
            if order.get("status") == "not_found":
                reasons.append("No order could be verified.")

            if order.get("is_delayed"):
                reasons.append("The customer's order is delayed.")
                actions.append("Investigate or update delivery status.")

        # Check billing investigation
        if billing:
            if billing.get("status") == "not_found":
                reasons.append("No payment record could be verified.")

            if billing.get("duplicate_charge"):
                reasons.append("A possible duplicate payment was detected.")
                actions.append("Initiate refund for duplicate charge.")

        # Unknown intent requires human assistance
        if investigation.get("intents") == ["unknown"]:
            return {
                "decision": "ESCALATE",
                "confidence": 0.40,
                "reason": "The customer's request could not be classified.",
                "reasons": ["Unknown support intent."],
                "recommended_actions": [
                    "Route the case to a human support agent."
                ],
                "human_context": self._build_human_context(
                    investigation,
                    ["Unknown support intent."],
                ),
            }

        # If nothing useful was found, escalate
        if not reasons:
            return {
                "decision": "ESCALATE",
                "confidence": 0.50,
                "reason": "The system could not determine a safe automated resolution.",
                "reasons": [
                    "Insufficient information for automatic resolution."
                ],
                "recommended_actions": [
                    "Review the case manually."
                ],
                "human_context": self._build_human_context(
                    investigation,
                    ["Insufficient information for automatic resolution."],
                ),
            }

        # Prototype rule:
        # A verified duplicate payment can be handled automatically.
        # A delayed order can also be investigated automatically.
        can_auto_resolve = True

        if order and order.get("status") == "not_found":
            can_auto_resolve = False

        if billing and billing.get("status") == "not_found":
            can_auto_resolve = False

        if can_auto_resolve:
            return {
                "decision": "RESOLVE",
                "confidence": 0.90,
                "reason": (
                    "The reported issues were verified and can be "
                    "handled through the available support actions."
                ),
                "reasons": reasons,
                "recommended_actions": actions,
                "human_context": None,
            }

        return {
            "decision": "ESCALATE",
            "confidence": 0.70,
            "reason": (
                "The system found an issue but does not have "
                "enough verified information to safely resolve it."
            ),
            "reasons": reasons,
            "recommended_actions": actions,
            "human_context": self._build_human_context(
                investigation,
                reasons,
            ),
        }

    def _build_human_context(
        self,
        investigation: Dict[str, Any],
        reasons,
    ) -> Dict[str, Any]:
        """
        Build the information that should accompany a human
        escalation so the customer does not have to repeat the issue.
        """

        return {
            "customer_id": investigation.get("customer_id"),
            "original_message": investigation.get("message"),
            "detected_intents": investigation.get("intents"),
            "investigation": {
                "order": investigation.get("order"),
                "billing": investigation.get("billing"),
            },
            "escalation_reasons": reasons,
            "next_step": "Human support agent review required.",
        }