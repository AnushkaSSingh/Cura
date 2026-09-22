from typing import Dict, Any, List
from datetime import datetime


class ConversationMemory:
    """
    Lightweight conversation memory for the Cura prototype.

    Stores recent support interactions in memory while the
    application is running.
    """

    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, Any]]] = {}

    def add_message(
        self,
        customer_id: str,
        role: str,
        message: str,
        metadata: Dict[str, Any] | None = None,
    ) -> None:
        """Store a customer or assistant message."""

        if customer_id not in self.sessions:
            self.sessions[customer_id] = []

        self.sessions[customer_id].append(
            {
                "role": role,
                "message": message,
                "metadata": metadata or {},
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    def get_history(
        self,
        customer_id: str,
    ) -> List[Dict[str, Any]]:
        """Return the customer's complete conversation history."""

        return self.sessions.get(customer_id, [])

    def get_recent_history(
        self,
        customer_id: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Return the most recent messages."""

        history = self.get_history(customer_id)

        return history[-limit:]

    def get_context(
        self,
        customer_id: str,
    ) -> Dict[str, Any]:
        """
        Return structured conversation context for the AI.
        """

        history = self.get_recent_history(customer_id)

        return {
            "customer_id": customer_id,
            "message_count": len(history),
            "recent_messages": history,
        }

    def clear(
        self,
        customer_id: str,
    ) -> None:
        """Clear stored conversation memory for a customer."""

        self.sessions.pop(customer_id, None)