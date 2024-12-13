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


@app.get("/api/product-details/{asin}")
async def product_details(asin: str, current_user: str = Depends(get_current_user)):
    """
    Ottiene i dettagli completi di un prodotto specifico dato l'ASIN.
    """
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    product = next((p for p in db_user.get("products", []) if p["asin"] == asin), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


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
    """
    Aggiunge un prodotto per l'utente corrente.
    """
    # Recupera l'utente dal database
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verifica che il prodotto non sia già monitorato
    for product in db_user.get("products", []):
        if product["product_url"] == request.product_url:
            raise HTTPException(status_code=400, detail="Product already being tracked")

    # Esegue scraping del prodotto
    product_data = fetch_product_data(request.product_url)
    if not product_data or not product_data.get("price"):
        raise HTTPException(status_code=400, detail="Error fetching product data")

    # Inizializza i dati del prodotto
    initial_price = float(product_data["price"])
    product_data["product_url"] = request.product_url
    product_data["category"] = request.category  # Aggiunge la categoria
    product_data["insertion_date"] = datetime.now().isoformat()
    product_data["price_history"] = [{"date": datetime.now().isoformat(), "price": initial_price}]
    product_data["max_price"] = initial_price
    product_data["min_price"] = initial_price
    product_data["average_price"] = initial_price

    # Aggiunge il prodotto al database dell'utente
    users_collection.update_one(
        {"_id": db_user["_id"]},
        {"$push": {"products": product_data}}
    )
    return {"message": "Product added successfully"}

@app.get("/api/product-details/{asin}")
async def product_details(asin: str, current_user: str = Depends(get_current_user)):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    product = next((p for p in db_user.get("products", []) if p["asin"] == asin), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "asin": product["asin"],
        "title": product["title"],
        "current_price": product["price"],
        "max_price": product["max_price"],
        "min_price": product["min_price"],
        "average_price": product["average_price"],
        "price_history": product["price_history"]
    }

@app.post("/api/update-prices-manual/")
async def update_prices_manual(current_user: str = Depends(get_current_user)):
    """Aggiorna manualmente i prezzi dei prodotti per l'utente corrente."""
    try:
        update_prices(user_filter=current_user)
        return {"message": "Price update triggered manually"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during manual price update")
    

def update_prices(user_filter=None, asin_filter=None):
    query = {"username": user_filter} if user_filter else {}
    users = users_collection.find(query)
    updated_products = []

    for user in users:
        products = user.get("products", [])
        for product in products:
            if asin_filter and product["asin"] not in asin_filter:
                continue

            try:
                updated_data = fetch_product_data(product["product_url"])
                if not updated_data or updated_data["price"] is None:
                    print(f"Product {product['asin']} is not available or has no price.")
                    product["availability"] = "Non disponibile"
                    continue

                new_price = float(updated_data["price"])
                product["price_history"].append({
                    "date": datetime.now().isoformat(),
                    "price": new_price
                })
                product["price"] = new_price
                product["availability"] = "Disponibile"

                # Calcola valori massimo, minimo e media
                price_history = product["price_history"]
                max_price_entry = max(price_history, key=lambda x: float(x["price"]))
                min_price_entry = min(price_history, key=lambda x: float(x["price"]))

                product["max_price"] = float(max_price_entry["price"])
                product["min_price"] = float(min_price_entry["price"])
                product["max_price_date"] = max_price_entry["date"]
                product["min_price_date"] = min_price_entry["date"]
                product["average_price"] = round(
                    sum(float(entry["price"]) for entry in price_history) / len(price_history), 2
                )

                updated_products.append(product["asin"])
                print(f"Price updated for ASIN {product['asin']}: {new_price}")

            except Exception as e:
                print(f"Error updating product {product['asin']}: {e}")
                continue

        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"products": products}}
        )

    return updated_products


scheduler = BackgroundScheduler()
scheduler.add_job(update_prices, 'interval', hours=5)
scheduler.start()




@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Amazon Price Tracker API"}
