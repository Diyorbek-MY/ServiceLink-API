# payments.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import random
from auth import get_current_user
from database import orders_db
from websocket_manager import notify_user

router = APIRouter(prefix="/payments", tags=["Payments"])

class PaymentRequest(BaseModel):
    order_id: int
    card_number: str
    expiry_date: str
    cvv: str

class PaymentResponse(BaseModel):
    order_id: int
    status: str
    message: str

@router.post("/process", response_model=PaymentResponse)
async def process_payment(
    payment: PaymentRequest,
    current_user: dict = Depends(get_current_user),
):
    order = next((o for o in orders_db if o["id"] == payment.order_id), None)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order["client"] != current_user["username"] and current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to pay for this order")
    
    # Fake payment gateway with a random success/failure
    payment_successful = random.choice([True, False])

    if payment_successful:
        order["status"] = "paid"
        message_client = f"Payment for Order {order['id']} was successful. The worker has been notified."
        message_worker = f"Order {order['id']} from {order['client']} has been paid. You can now begin work."
        
        await notify_user(order["client"], message_client)
        await notify_user(order["worker"], message_worker)
        
        return PaymentResponse(
            order_id=order["id"],
            status="paid",
            message=message_client
        )
    else:
        order["status"] = "canceled"
        message_client = f"Payment for Order {order['id']} failed. Please try again."
        
        await notify_user(order["client"], message_client)

        return PaymentResponse(
            order_id=order["id"],
            status="canceled",
            message=message_client
        )