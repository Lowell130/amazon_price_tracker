from fastapi import APIRouter, HTTPException, Query
from app.db import public_alerts_collection, users_collection
from app.schemas import GuestAlertSubscription
from datetime import datetime
import re

router = APIRouter(prefix="/api/public", tags=["public"])

@router.post("/subscribe-alert")
async def subscribe_to_price_alert(data: GuestAlertSubscription):
    existing = public_alerts_collection.find_one({"email": data.email, "asin": data.asin})
    if existing:
        return {"message": "Hai già richiesto un avviso per questo prodotto."}

    try:
        public_alerts_collection.insert_one({
            "email": data.email,
            "asin": data.asin,
            "subscribed_at": datetime.utcnow()
        })
        return {"message": "Iscrizione completata. Ti avviseremo in caso di ribasso di prezzo!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Errore interno del server.")

@router.delete("/unsubscribe-alert")
async def unsubscribe_alert(email: str = Query(...), asin: str = Query(...)):
    result = public_alerts_collection.delete_one({"email": email, "asin": asin})
    if result.deleted_count == 1:
        return {"message": "Sottoscrizione cancellata con successo."}
    else:
        raise HTTPException(status_code=404, detail="Nessuna sottoscrizione trovata.")

@router.get("/check-subscription")
async def check_subscription(email: str = Query(...), asin: str = Query(...)):
    exists = public_alerts_collection.find_one({"email": email, "asin": asin})
    return {"subscribed": bool(exists)}

@router.get("/search-products")
async def search_products(title: str = Query(..., min_length=2)):
    try:
        words = title.lower().split()
        regex_conditions = [{"$regexMatch": {"input": "$$product.title", "regex": rf"\b{word}\b", "options": "i"}} for word in words]

        products_cursor = users_collection.aggregate([
            {
                "$project": {
                    "filtered_products": {
                        "$filter": {
                            "input": "$products",
                            "as": "product",
                            "cond": { "$and": regex_conditions }
                        }
                    }
                }
            },
            {"$unwind": "$filtered_products"}
        ])

        all_products = [doc["filtered_products"] for doc in products_cursor]

        if not all_products:
            raise HTTPException(status_code=404, detail="Nessun prodotto trovato.")

        for product in all_products:
            old_price = product.get("old_price")
            new_price = product.get("new_price") or product.get("price")
            if old_price and new_price:
                try:
                    product["price_drop"] = round(old_price - new_price, 2)
                except:
                    product["price_drop"] = None
            else:
                product["price_drop"] = None

        return {"products": all_products}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nella ricerca: {str(e)}")

@router.get("/product-details/{asin}")
async def public_product_details(asin: str):
    product = users_collection.find_one({"products.asin": asin}, {"products.$": 1})
    
    if not product or "products" not in product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product["products"][0]

@router.get("/price-drops")
async def get_price_drops(
    category: str = None,
    limit: int = Query(64, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    try:
        price_drops_collection = users_collection.database["price_drops"]
        price_drops_data = price_drops_collection.find_one(sort=[("generation_date", -1)])
        
        if not price_drops_data:
            raise HTTPException(status_code=404, detail="No price drops found.")

        drops = price_drops_data["drops"]
        
        if category:
            drops = [drop for drop in drops if drop.get("category") == category]
        
        drops = [drop for drop in drops if drop.get("condition") != "Non disponibile"]
        drops.sort(key=lambda x: x.get("price_drop", 0), reverse=True)

        total_drops = len(drops)
        drops = drops[skip : skip + limit]

        return {
            "total_drops": total_drops,
            "displayed_drops": len(drops),
            "data": drops
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving price drops: {str(e)}")
