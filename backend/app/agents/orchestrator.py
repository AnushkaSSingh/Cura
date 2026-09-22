from typing import Dict, Any

from .order_agent import OrderAgent
from .billing_agent import BillingAgent
from .escalation_agent import EscalationAgent


class SupportOrchestrator:
    """
    Main AI support coordinator.

    Receives a customer message, identifies the issues involved,
    delegates investigation to specialized agents, and decides
    whether the case can be resolved or should be escalated.
    """

    def __init__(self):
        self.order_agent = OrderAgent()
        self.billing_agent = BillingAgent()
        self.escalation_agent = EscalationAgent()

    def analyze_intent(self, message: str) -> Dict[str, Any]:
        """
        Identify the major support issues present in the message.

        This prototype uses simple keyword-based intent detection.
        The LLM layer can later replace or enhance this.
        """

        message_lower = message.lower()

        intents = []

        order_keywords = [
            "order",
            "delivery",
            "delivered",
            "late",
            "delayed",
            "shipping",
            "shipment",
            "package",
            "parcel",
        ]

        billing_keywords = [
            "charged",
            "charge",
            "payment",
            "paid",
            "billing",
            "refund",
            "duplicate",
            "twice",
            "money",
        ]

        if any(keyword in message_lower for keyword in order_keywords):
            intents.append("order")

        if any(keyword in message_lower for keyword in billing_keywords):
            intents.append("billing")

        if not intents:
            intents.append("unknown")

        return {
            "intents": intents,
            "message": message,
        }

    def investigate(
        self,
        customer_id: str,
        message: str,
    ) -> Dict[str, Any]:
        """
        Investigate the customer's issue using the appropriate agents.
        """

        intent_result = self.analyze_intent(message)
        intents = intent_result["intents"]

        investigation = {
            "customer_id": customer_id,
            "message": message,
            "intents": intents,
            "order": None,
            "billing": None,
        }

        if "order" in intents:
            investigation["order"] = self.order_agent.investigate(
                customer_id=customer_id,
                message=message,
            )

        if "billing" in intents:
            investigation["billing"] = self.billing_agent.investigate(
                customer_id=customer_id,
                message=message,
            )

        return investigation

    def decide_next_step(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Decide whether the case can be resolved automatically
        or requires human escalation.
        """

        return self.escalation_agent.evaluate(investigation)

    def handle_request(
        self,
        customer_id: str,
        message: str,
    ) -> Dict[str, Any]:
        """
        Complete support workflow:

        1. Understand customer intent
        2. Investigate relevant systems
        3. Decide whether to resolve or escalate
        """

        investigation = self.investigate(
            customer_id=customer_id,
            message=message,
        )

        decision = self.decide_next_step(investigation)

        return {
            "customer_id": customer_id,
            "message": message,
            "investigation": investigation,
            "decision": decision,
        }