import os
from typing import Dict, Any


class LLMService:
    """
    LLM interface for Cura.

    The prototype keeps the LLM integration isolated so the
    rest of the application does not depend directly on a
    specific AI provider.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    def is_configured(self) -> bool:
        """Check whether an LLM API key is available."""

        return bool(self.api_key)

    def build_support_prompt(
        self,
        customer_message: str,
        customer_context: Dict[str, Any],
        investigation: Dict[str, Any],
    ) -> str:
        """
        Build the context that would be sent to the LLM
        for generating a support response.
        """

        return f"""
You are Cura, an autonomous customer support agent.

Customer message:
{customer_message}

Customer context:
{customer_context}

Investigation:
{investigation}

Your job is to:
1. Understand the customer's problem.
2. Use the investigation results.
3. Explain what was found clearly.
4. Mention actions taken or recommended.
5. Escalate when the system cannot safely resolve the issue.
6. Never invent information that is not present in the investigation.

Generate a concise and helpful customer support response.
""".strip()

    def generate_response(
        self,
        customer_message: str,
        customer_context: Dict[str, Any],
        investigation: Dict[str, Any],
    ) -> str:
        """
        Generate a prototype response.

        The actual provider call can be connected here later.
        """

        decision = investigation.get("decision", {})
        decision_type = decision.get("decision")

        if decision_type == "RESOLVE":
            return (
                "I investigated your request and found the relevant "
                "issue in our support records. The available automated "
                "support action can now be processed."
            )

        if decision_type == "ESCALATE":
            return (
                "I've investigated the information available for your "
                "case. Because this requires additional review, I'm "
                "escalating it to a human support agent with the "
                "investigation and conversation context attached."
            )

        return (
            "I've received your request and am reviewing the "
            "available information."
        )