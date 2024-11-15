# app/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import bcrypt
import jwt
import json
import os
from datetime import datetime, timedelta
from typing import Optional
from app.config import SECRET_KEY
from app.crud import get_user_products, add_product_to_user, remove_product_from_user  # Importa la funzione per aggiungere prodotti

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

# Modello per la richiesta di aggiunta di un prodotto
class ProductRequest(BaseModel):
    product_url: str

# Funzione helper per registrare un nuovo utente
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

# Endpoint per ottenere i dati della dashboard
@router.get("/dashboard")
async def dashboard(current_user: str = Depends(get_current_user)):
    try:
        products = get_user_products(current_user)
        return {"products": products}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Errore nel caricamento della dashboard")

# Endpoint per aggiungere un prodotto
@router.post("/add-product/")
async def add_product(request: ProductRequest, current_user: str = Depends(get_current_user)):
    try:
        result = add_product_to_user(current_user, request.product_url)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Errore interno del server")


# Endpoint per eliminare un prodotto monitorato dall'utente
@router.delete("/remove-product/{asin}")
async def remove_product(asin: str, current_user: str = Depends(get_current_user)):
    try:
        result = remove_product_from_user(current_user, asin)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Errore durante l'eliminazione del prodotto")
    


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
