# orders.py
from fastapi import APIRouter, HTTPException, Depends, status
from database import orders_db, users_db
from models import OrderCreate, OrderResponse
from auth import get_current_user
from websocket_manager import notify_user

router = APIRouter(tags=["Orders"])

def calculate_service_fee(amount: float) -> float:
    """Calculates a 10% service fee."""
    return amount * 0.10

@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate, current_user: dict = Depends(get_current_user)):
    """Allows a client to create a new order."""
    if current_user["role"] != "client":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only clients can create orders")

    service_fee = calculate_service_fee(order.amount)
    total_amount = order.amount + service_fee
    
    order_id = len(orders_db) + 1
    new_order = {
        "id": order_id,
        "client": current_user["username"],
        "worker": order.worker,
        "specialty": order.specialty,
        "amount": total_amount,
        "status": "pending"
    }
    orders_db.append(new_order)
    
    await notify_user(order.worker, f"You have a new order from {current_user['username']}! Total amount: ${total_amount:.2f}")
    await notify_user(current_user["username"], "Your order has been successfully created.")
    
    return new_order

@router.get("/orders/me", response_model=list[OrderResponse])
def get_my_orders(current_user: dict = Depends(get_current_user)):
    """Retrieves order history based on the user's role."""
    if current_user["role"] == "client":
        return [order for order in orders_db if order["client"] == current_user["username"]]
    
    elif current_user["role"] == "worker":
        worker_info = users_db.get(current_user["username"])
        if not worker_info or "specialty" not in worker_info:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Worker specialty not defined.")
        
        worker_specialty = worker_info["specialty"]
        
        # Filter orders by the worker's specialty
        return [order for order in orders_db if order["specialty"] == worker_specialty]
        
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this history.")

@router.get("/orders", response_model=list[OrderResponse])
def get_all_orders(current_user: dict = Depends(get_current_user)):
    """Retrieves all orders (admin-only)."""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions to view all orders.")
    return orders_db