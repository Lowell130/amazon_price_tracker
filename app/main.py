#main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router, get_current_user
from app.scraper import fetch_product_data
from app.db import users_collection
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from bson.objectid import ObjectId
from typing import List
from typing import Optional  # Aggiunto import

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://amazon-price-tracker-delta.vercel.app"
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

class ProductRequest(BaseModel):
    product_url: str
    category: Optional[str] = None  # Campo facoltativo per la categoria

@app.post("/api/update-selected-prices/")
async def update_selected_prices(
    asin_list: List[str],  # Riceve una lista di ASIN dal body della richiesta
    current_user: str = Depends(get_current_user)
):
    """Aggiorna manualmente i prezzi solo per i prodotti selezionati dall'utente."""
    if not asin_list:
        raise HTTPException(status_code=400, detail="ASIN list cannot be empty")

    try:
        updated_products = update_prices(user_filter=current_user, asin_filter=asin_list)
        return {"message": "Selected product prices updated", "updated_products": updated_products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating selected products: {str(e)}")

@app.post("/api/add-product/")
async def add_product(request: ProductRequest, current_user: str = Depends(get_current_user)):
    """Aggiunge un prodotto per l'utente corrente."""
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verifica che il prodotto non sia già monitorato
    for product in db_user.get("products", []):
        if product["product_url"] == request.product_url:
            raise HTTPException(status_code=400, detail="Product already being tracked")

    # Recupera i dati del prodotto
    product_data = fetch_product_data(request.product_url)
    if not product_data:
        raise HTTPException(status_code=400, detail="Error fetching product data")
    
    product_data["product_url"] = request.product_url
    product_data["category"] = request.category  # Salva la categoria
    product_data["insertion_date"] = datetime.now().isoformat()
    product_data["price_history"] = [{"date": datetime.now().isoformat(), "price": product_data["price"]}]

    # Aggiungi il prodotto all'utente
    users_collection.update_one(
        {"_id": db_user["_id"]},
        {"$push": {"products": product_data}}
    )
    return {"message": "Product added successfully"}


@app.get("/api/price-history/{asin}")
async def price_history(asin: str, current_user: str = Depends(get_current_user)):
    """Ottiene la cronologia dei prezzi per un prodotto specifico."""
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    product = next((p for p in db_user.get("products", []) if p["asin"] == asin), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product["price_history"]

@app.post("/api/update-prices-manual/")
async def update_prices_manual(current_user: str = Depends(get_current_user)):
    """Aggiorna manualmente i prezzi dei prodotti per l'utente corrente."""
    try:
        update_prices(user_filter=current_user)
        return {"message": "Price update triggered manually"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during manual price update")
    



def update_prices(user_filter=None, asin_filter=None):
    """
    Aggiorna il prezzo dei prodotti per tutti gli utenti o solo per un utente specifico e un elenco di ASIN.
    :param user_filter: Stringa per filtrare un utente specifico.
    :param asin_filter: Lista di ASIN per aggiornare solo prodotti specifici.
    """
    # Filtra utenti (opzionale)
    query = {"username": user_filter} if user_filter else {}
    users = users_collection.find(query)
    updated_products = []  # Per tracciare gli ASIN aggiornati

    for user in users:
        products = user.get("products", [])
        for product in products:
            # Filtra solo i prodotti con ASIN specificati
            if asin_filter and product["asin"] not in asin_filter:
                continue

            try:
                # Fetch dati aggiornati dal prodotto
                updated_data = fetch_product_data(product["product_url"])
                if not updated_data:
                    print(f"Price not available for ASIN {product['asin']}, skipping update")
                    continue

                # Aggiorna prezzo e storico dei prezzi
                new_price = updated_data["price"]
                product["price_history"].append({
                    "date": datetime.now().isoformat(),
                    "price": new_price
                })
                product["price"] = new_price
                updated_products.append(product["asin"])  # Aggiungi ASIN aggiornato alla lista
                print(f"Price updated for ASIN {product['asin']}: {new_price}")

            except Exception as e:
                print(f"Error updating product {product['asin']}: {e}")
                continue

        # Aggiorna i prodotti nel database
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"products": products}}
        )

    return updated_products  # Restituisce gli ASIN aggiornati


scheduler = BackgroundScheduler()
scheduler.add_job(update_prices, 'interval', hours=12)
scheduler.start()




@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Amazon Price Tracker API"}
