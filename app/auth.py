#auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.config import SECRET_KEY
from app.db import users_collection  # Collezione MongoDB per gli utenti
from bson.objectid import ObjectId
from app.scraper import fetch_product_data
# from app.main import send_email
from datetime import datetime, timedelta
import random
import string
from fastapi.responses import JSONResponse
from app.utils.email import send_email
import os  # Importa il modulo os per accedere alle variabili d'ambiente
import re 




router = APIRouter()

# Configurazione per il sistema di autenticazione con token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Modelli Pydantic
class User(BaseModel):
    username: str
    password: str
    email: Optional[str] = None  # Campo opzionale, solo per registrazione

class UserLogin(BaseModel):
    login: str  # Può essere username o email
    password: str


class UserInDB(User):
    hashed_password: str

class ProductRequest(BaseModel):
    product_url: str

class PasswordResetRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


def validate_password(password: str) -> bool:
    """Verifica se la password soddisfa i requisiti di sicurezza."""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

@router.post("/register")
async def register(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    if not validate_password(user.password):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long, "
                   "contain an uppercase letter, a lowercase letter, "
                   "a number, and a special character."
        )

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "products": []
    }
    users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}

# Login e generazione token JWT
@router.post("/login")
async def login(user: UserLogin):
    db_user = users_collection.find_one(
        {"$or": [{"username": user.login}, {"email": user.login}]}
    )
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user["hashed_password"].encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid login or password")

    token = jwt.encode({
        "sub": db_user["username"],
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

# Endpoint per ottenere i dati della dashboard
@router.get("/dashboard")
async def dashboard(current_user: str = Depends(get_current_user)):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"products": db_user.get("products", [])}

# Endpoint per eliminare un prodotto monitorato dall'utente
@router.delete("/remove-product/{asin}")
async def remove_product(asin: str, current_user: str = Depends(get_current_user)):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_products = [p for p in db_user.get("products", []) if p["asin"] != asin]
    if len(updated_products) == len(db_user.get("products", [])):
        raise HTTPException(status_code=404, detail="Product not found")

    users_collection.update_one(
        {"_id": db_user["_id"]},
        {"$set": {"products": updated_products}}
    )
    return {"message": "Product removed successfully"}

# Refresh del token
@router.post("/refresh-token")
async def refresh_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Token non valido")

        new_token = jwt.encode({
            "sub": username,
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }, SECRET_KEY, algorithm="HS256")

        return {"access_token": new_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token scaduto")
    


# Genera un token casuale
def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# Mappa per i token di recupero password (può essere spostato su una collezione MongoDB)
password_reset_tokens = {}

# Genera un link di reset utilizzando l'URL base dall'ambiente
@router.post("/request-password-reset")
async def request_password_reset(request: PasswordResetRequest):
    user = users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Genera un token di reset e salva nella mappa
    reset_token = generate_reset_token()
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    password_reset_tokens[reset_token] = {"email": request.email, "expires_at": expiration_time}

    # Usa l'URL del frontend
    frontend_base_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:8080")
    reset_link = f"{frontend_base_url}/reset-password?token={reset_token}"

    # Invia email all'utente
    send_email(
        request.email,
        "Password Reset Request",
        f"Usa il seguente link per reimpostare la tua password: {reset_link}\n"
        f"Il link scade in un'ora."
    )

    return {"message": "Password reset email sent"}



@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    token = request.token
    new_password = request.new_password

    # Controlla se il token esiste e non è scaduto
    reset_data = password_reset_tokens.get(token)
    if not reset_data or reset_data["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    email = reset_data["email"]
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Hash della nuova password
    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    users_collection.update_one({"email": email}, {"$set": {"hashed_password": hashed_password}})

    # Rimuovi il token usato
    del password_reset_tokens[token]

    return {"message": "Password reset successfully"}