# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware  # Importa CORSMiddleware
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

# Configura le origini consentite
origins = [
    "http://localhost:8080",  # Origine del server di sviluppo Vue
    "http://127.0.0.1:8080"
]

# Aggiungi CORSMiddleware per consentire le richieste dal frontend Vue
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Consente solo le origini specificate
    allow_credentials=True,
    allow_methods=["*"],  # Consente tutti i metodi (GET, POST, ecc.)
    allow_headers=["*"],  # Consente tutti gli header
)

# Configurazione per il sistema di autenticazione con token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Includiamo le rotte di autenticazione
app.include_router(auth_router, prefix="/api")

# Directory dei file JSON degli utenti
USER_DATA_DIR = "data/users"

# Definizione del modello Pydantic per il corpo della richiesta di aggiunta prodotto
class ProductRequest(BaseModel):
    product_url: str

@app.post("/add-product/")
async def add_product(request: ProductRequest, current_user: str = Depends(get_current_user)):
    try:
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
                try:
                    updated_data = fetch_product_data(f"https://www.amazon.com/dp/{product['asin']}")
                    if updated_data is None:
                        print(f"Prezzo non disponibile per ASIN {product['asin']}, salto aggiornamento")
                        continue

                    new_price = updated_data["price"]

                    # Aggiorna lo storico dei prezzi solo se è disponibile un nuovo prezzo valido
                    product["price_history"].append({
                        "date": updated_data["extraction_date"],
                        "price": new_price
                    })

                    # Aggiorna il prezzo corrente
                    product["price"] = new_price

                except Exception as e:
                    print(f"Errore durante l'aggiornamento del prodotto {product['asin']}: {e}")
                    continue  # Ignora e passa al prodotto successivo

            # Scrivi i dati aggiornati sul file JSON
            f.seek(0)
            json.dump(user_data, f, indent=4)
            f.truncate()

# Inizializzazione del job scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(update_prices, 'interval', hours=1) 
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Amazon Price Tracker API"}
