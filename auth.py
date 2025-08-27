# auth.py
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional, Dict

from models import UserRegister, UserResponse, Token
from database import users_db

router = APIRouter()

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------- JWT Utils --------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = users_db.get(username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -------- Routes --------
@router.post("/register", response_model=UserResponse)
def register(user: UserRegister):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    if user.role not in ["client", "worker", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    users_db[user.username] = {"username": user.username,
                               "password": user.password,
                               "role": user.role}
    return {"username": user.username, "role": user.role}

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(
        {"sub": user["username"], "role": user["role"]},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "role": current_user["role"]}

@router.get("/users", response_model=list[UserResponse])
def get_all_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return [{"username": u["username"], "role": u["role"]} for u in users_db.values()]
