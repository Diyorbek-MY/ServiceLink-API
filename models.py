# models.py
from pydantic import BaseModel
from typing import Optional

# -------- Users --------
class UserRegister(BaseModel):
    username: str
    password: str
    role: str   # client, worker, admin

class UserResponse(BaseModel):
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

# -------- Orders --------
class OrderCreate(BaseModel):
    client: str
    worker: str
    specialty: str
    amount: float

class OrderResponse(BaseModel):
    id: int
    client: str
    worker: str
    specialty: str
    amount: float
    status: str
