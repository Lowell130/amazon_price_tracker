from fastapi import APIRouter, HTTPException, Query, Depends
from app.db import get_public_alerts_collection, get_users_collection, get_products_collection
from app.schemas import GuestAlertSubscription
from datetime import datetime
import re

router = APIRouter(prefix="/api/public", tags=["public"])

@router.post("/subscribe-alert")
async def subscribe_to_price_alert(data: GuestAlertSubscription, public_alerts_collection = Depends(get_public_alerts_collection)):
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
async def unsubscribe_alert(email: str = Query(...), asin: str = Query(...), public_alerts_collection = Depends(get_public_alerts_collection)):
    result = public_alerts_collection.delete_one({"email": email, "asin": asin})
    if result.deleted_count == 1:
        return {"message": "Sottoscrizione cancellata con successo."}
    else:
        raise HTTPException(status_code=404, detail="Nessuna sottoscrizione trovata.")

@router.get("/check-subscription")
async def check_subscription(email: str = Query(...), asin: str = Query(...), public_alerts_collection = Depends(get_public_alerts_collection)):
    exists = public_alerts_collection.find_one({"email": email, "asin": asin})
    return {"subscribed": bool(exists)}

@router.get("/search-products")
async def search_products(title: str = Query(..., min_length=2), products_collection = Depends(get_products_collection)):
    try:
        words = title.lower().split()
        regex_conditions = [{"title": {"$regex": rf"\b{word}\b", "$options": "i"}} for word in words]

        # Cerca i prodotti corrispondenti nella collezione globale (limita i risultati)
        products_cursor = products_collection.find({"$and": regex_conditions}).limit(50)

        all_products = list(products_cursor)

        if not all_products:
            raise HTTPException(status_code=404, detail="Nessun prodotto trovato.")

        for product in all_products:
            if "_id" in product:
                del product["_id"]
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
async def public_product_details(asin: str, products_collection = Depends(get_products_collection)):
    product = products_collection.find_one({"asin": asin})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if "_id" in product:
        del product["_id"]
        
    # Override affiliate link with current tag
    from app.config import AFFILIATE_TAG
    product["affiliate"] = f"https://www.amazon.it/gp/product/{asin}/?tag={AFFILIATE_TAG}"
    
    return product

@router.get("/price-drops")
async def get_price_drops(
    category: str = None,
    limit: int = Query(64, ge=1, le=100),
    skip: int = Query(0, ge=0),
    users_collection = Depends(get_users_collection)
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

        # Ensure all drops have the correct affiliate link
        from app.config import AFFILIATE_TAG
        for drop in drops:
            asin = drop.get("asin")
            if asin:
                drop["affiliate"] = f"https://www.amazon.it/gp/product/{asin}/?tag={AFFILIATE_TAG}"

        return {
            "total_drops": total_drops,
            "displayed_drops": len(drops),
            "data": drops
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving price drops: {str(e)}")
