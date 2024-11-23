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
    product_data["product_url"] = request.product_url
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

def update_prices(user_filter=None):
    """Aggiorna il prezzo dei prodotti per tutti gli utenti o per un utente specifico."""
    query = {"username": user_filter} if user_filter else {}
    users = users_collection.find(query)

    for user in users:
        products = user.get("products", [])
        for product in products:
            try:
                updated_data = fetch_product_data(product["product_url"])
                if not updated_data:
                    print(f"Price not available for ASIN {product['asin']}, skipping update")
                    continue

                new_price = updated_data["price"]
                product["price_history"].append({
                    "date": datetime.now().isoformat(),
                    "price": new_price
                })
                product["price"] = new_price
                print(f"Price updated for ASIN {product['asin']}: {new_price}")

            except Exception as e:
                print(f"Error updating product {product['asin']}: {e}")
                continue

        # Aggiorna i prodotti dell'utente nel database
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"products": products}}
        )

scheduler = BackgroundScheduler()
scheduler.add_job(update_prices, 'interval', hours=5)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Amazon Price Tracker API"}
