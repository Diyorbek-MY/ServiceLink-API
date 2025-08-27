# main.py
from fastapi import FastAPI
from auth import router as auth_router
from orders import router as orders_router
from payments import router as payments_router
from websocket_manager import ws_router, notify_user # Correct import here

app = FastAPI()

# Routers
app.include_router(auth_router, tags=["Auth"])
app.include_router(orders_router, tags=["Orders"])
app.include_router(payments_router, tags=["Payments"])
app.include_router(ws_router, tags=["WebSocket"])