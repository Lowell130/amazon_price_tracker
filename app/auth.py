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


router = APIRouter()

# Configurazione per il sistema di autenticazione con token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Modelli Pydantic
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

class ProductRequest(BaseModel):
    product_url: str

# Registrazione
@router.post("/register")
async def register(user: User):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = {
        "username": user.username,
        "hashed_password": hashed_password,
        "products": []
    }
    users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}

# Login e generazione token JWT
@router.post("/login")
async def login(user: User):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user["hashed_password"].encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid username or password")

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

# # Endpoint per aggiungere un prodotto
# @router.post("/add-product/")
# async def add_product(request: ProductRequest, current_user: str = Depends(get_current_user)):
#     db_user = users_collection.find_one({"username": current_user})
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Verifica che il prodotto non sia già monitorato
#     for product in db_user.get("products", []):
#         if product["product_url"] == request.product_url:
#             raise HTTPException(status_code=400, detail="Product already being tracked")

#     # Recupera i dati del prodotto
#     product_data = fetch_product_data(request.product_url)
#     product_data["product_url"] = request.product_url
#     product_data["insertion_date"] = datetime.now().isoformat()
#     product_data["price_history"] = [{"date": datetime.now().isoformat(), "price": product_data["price"]}]

#     # Aggiungi il prodotto all'utente
#     users_collection.update_one(
#         {"_id": db_user["_id"]},
#         {"$push": {"products": product_data}}
#     )
#     return {"message": "Product added successfully"}

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
