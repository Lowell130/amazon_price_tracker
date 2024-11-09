# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.auth import router as auth_router, get_current_user
from app.crud import add_product_to_user, get_price_history
from app.scraper import fetch_product_data
from pydantic import BaseModel  # Import per il modello Pydantic
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
from datetime import datetime
import app.config as config

app = FastAPI()

# Configurazione per il sistema di autenticazione con token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Includiamo le rotte di autenticazione
app.include_router(auth_router)

# Directory dei file JSON degli utenti
USER_DATA_DIR = "data/users"

# Definizione del modello Pydantic per il corpo della richiesta di aggiunta prodotto
class ProductRequest(BaseModel):
    product_url: str

@app.post("/add-product/")
async def add_product(request: ProductRequest, current_user: str = Depends(get_current_user)):
    try:
        # Utilizza il product_url dal corpo JSON della richiesta
        result = add_product_to_user(current_user, request.product_url)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Errore interno del server")

@app.get("/price-history/{asin}")
async def price_history(asin: str, current_user: str = Depends(get_current_user)):
    try:
        history = get_price_history(current_user, asin)
        return history
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Errore interno del server")

def update_prices():
    """Aggiorna il prezzo di tutti i prodotti monitorati per ogni utente."""
    for user_file in os.listdir(USER_DATA_DIR):
        user_path = os.path.join(USER_DATA_DIR, user_file)
        with open(user_path, "r+") as f:
            user_data = json.load(f)
            for product in user_data.get("products", []):
                # Recupera i dati aggiornati tramite scraping
                updated_data = fetch_product_data(f"https://www.amazon.com/dp/{product['asin']}")
                new_price = updated_data["price"]
                
                # Aggiorna lo storico dei prezzi
                product["price_history"].append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "price": new_price
                })
                
                # Aggiorna il prezzo corrente
                product["price"] = new_price
            
            # Scrivi i dati aggiornati sul file JSON
            f.seek(0)
            json.dump(user_data, f, indent=4)
            f.truncate()

# Inizializzazione del job scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(update_prices, 'interval', hours=24)  # Esegue il job ogni 24 ore
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Amazon Price Tracker API"}
