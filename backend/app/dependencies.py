from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY
from app.db import users_collection
import jwt
import random
import string
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login") # Updated tokenUrl

# In-memory storage for reset tokens (consider moving to DB)
password_reset_tokens = {}

def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

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

def admin_required(current_user: str = Depends(get_current_user)):
    user = users_collection.find_one({"username": current_user})
    if not user or not user.get("admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required"
        )
    return user
