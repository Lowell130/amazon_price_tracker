# app/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
import bcrypt
import jwt
import json
import os
from datetime import datetime, timedelta
from app.config import SECRET_KEY

router = APIRouter()

# Configurazione per il sistema di autenticazione con token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Directory dove vengono salvati i dati utente
USER_DATA_DIR = "data/users"

# Modelli Pydantic
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

# Helper per registrare un nuovo utente
def create_user_file(username, hashed_password):
    user_data = {
        "username": username,
        "hashed_password": hashed_password,
        "products": []
    }
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    with open(f"{USER_DATA_DIR}/{username}.json", "w") as f:
        json.dump(user_data, f)

# Registrazione
@router.post("/register")
async def register(user: User):
    user_file = f"{USER_DATA_DIR}/{user.username}.json"
    if os.path.exists(user_file):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    create_user_file(user.username, hashed_password.decode("utf-8"))
    return {"message": "User registered successfully"}

# Login e generazione token JWT
@router.post("/login")
async def login(user: User):
    user_file = f"{USER_DATA_DIR}/{user.username}.json"
    if not os.path.exists(user_file):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    with open(user_file, "r") as f:
        user_data = json.load(f)
    
    if not bcrypt.checkpw(user.password.encode("utf-8"), user_data["hashed_password"].encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    token = jwt.encode({
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }, SECRET_KEY, algorithm="HS256")
    
    return {"access_token": token, "token_type": "bearer"}

# Funzione per ottenere l'utente corrente tramite JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token non valido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token scaduto",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token non valido",
            headers={"WWW-Authenticate": "Bearer"},
        )
