from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import User, UserLogin, PasswordResetRequest, ResetPasswordRequest
from app.dependencies import get_current_user, oauth2_scheme, password_reset_tokens, generate_reset_token
from app.db import users_collection
from app.config import SECRET_KEY
from app.utils.email import send_email
import bcrypt
import jwt
from datetime import datetime, timedelta
import re
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])

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

@router.post("/login")
async def login(user: UserLogin):
    db_user = users_collection.find_one(
        {"$or": [{"username": user.login}, {"email": user.login}]}
    )
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user["hashed_password"].encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid login or password")

    token = jwt.encode({
        "sub": db_user["username"],
        "admin": db_user.get("admin", False),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }, SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}

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

@router.get("/users/me")
async def get_user_info(current_user: str = Depends(get_current_user)):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": db_user["username"],
        "email": db_user.get("email"),
        "admin": db_user.get("admin", False),
        "products_count": len(db_user.get("products", []))
    }

