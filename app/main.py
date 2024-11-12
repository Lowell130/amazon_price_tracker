# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router, get_current_user
from app.crud import add_product_to_user, get_price_history
from app.scraper import fetch_product_data
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
from datetime import datetime
import app.config as config

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(auth_router, prefix="/api")

USER_DATA_DIR = "data/users"

class ProductRequest(BaseModel):
    product_url: str

@app.post("/api/add-product/")
async def add_product(request: ProductRequest, current_user: str = Depends(get_current_user)):
    try:
        result = add_product_to_user(current_user, request.product_url)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Errore interno del server")

@app.get("/api/price-history/{asin}")
async def price_history(asin: str, current_user: str = Depends(get_current_user)):
    try:
        history = get_price_history(current_user, asin)
        return history
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Errore interno del server")

@app.post("/api/update-prices-manual/")
async def update_prices_manual(current_user: str = Depends(get_current_user)):
    """Endpoint per avviare manualmente l'aggiornamento dei prezzi."""
    try:
        update_prices(user_filter=current_user)
        return {"message": "Aggiornamento dei prezzi avviato manualmente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Errore durante l'aggiornamento manuale")

def update_prices(user_filter=None):
    """Aggiorna il prezzo di tutti i prodotti monitorati per ogni utente o solo per l'utente specificato."""
    for user_file in os.listdir(USER_DATA_DIR):
        if user_filter and not user_file.startswith(user_filter):
            continue
        user_path = os.path.join(USER_DATA_DIR, user_file)
        with open(user_path, "r+") as f:
            user_data = json.load(f)
            for product in user_data.get("products", []):
                try:
                    updated_data = fetch_product_data(product["product_url"])
                    if updated_data is None:
                        print(f"Prezzo non disponibile per ASIN {product['asin']}, salto aggiornamento")
                        continue

                    new_price = updated_data["price"]
                    last_price = product["price_history"][-1]["price"] if product["price_history"] else None

                    product["price_history"].append({
                        "date": updated_data["extraction_date"],
                        "price": new_price
                    })
                    product["price"] = new_price
                    print(f"Prezzo aggiornato per ASIN {product['asin']}: {new_price}")

                except Exception as e:
                    print(f"Errore durante l'aggiornamento del prodotto {product['asin']}: {e}")
                    continue

            f.seek(0)
            json.dump(user_data, f, indent=4)
            f.truncate()

scheduler = BackgroundScheduler()
scheduler.add_job(update_prices, 'interval', hours=1)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Amazon Price Tracker API"}
