from fastapi import APIRouter, HTTPException

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.customer_service import CustomerService
from backend.app.services.order_service import OrderService
from backend.app.services.payment_service import PaymentService
from backend.app.services.ticket_service import TicketService
from backend.app.services.escalation_service import EscalationService


router = APIRouter(prefix="/chat", tags=["Chat"])

customer_service = CustomerService()
order_service = OrderService()
payment_service = PaymentService()
ticket_service = TicketService()
escalation_service = EscalationService()


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    customer = customer_service.get_customer(request.customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    message = request.message.lower()

    if "order" in message:
        order = order_service.get_latest_customer_order(
            request.customer_id
        )

        return ChatResponse(
            customer_id=request.customer_id,
            message="Here is your latest order information.",
            intent="order_status",
            data=order,
        )

    if "payment" in message or "billing" in message:
        payments = payment_service.get_customer_payments(
            request.customer_id
        )

        return ChatResponse(
            customer_id=request.customer_id,
            message="Here is your payment information.",
            intent="payment",
            data={"payments": payments},
        )

    if "ticket" in message:
        tickets = ticket_service.get_customer_tickets(
            request.customer_id
        )

        return ChatResponse(
            customer_id=request.customer_id,
            message="Here is your ticket information.",
            intent="ticket",
            data={"tickets": tickets},
        )

    if "escalate" in message or "human" in message:
        escalation = escalation_service.create_escalation(
            customer_id=request.customer_id,
            reason=request.message,
        )

        return ChatResponse(
            customer_id=request.customer_id,
            message="Your issue has been escalated for human review.",
            intent="escalation",
            data=escalation,
            escalated=True,
        )

    return ChatResponse(
        customer_id=request.customer_id,
        message="I could not identify the type of request.",
        intent="unknown",
    )