from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import List
from app.schemas import ProductRequest
from app.dependencies import get_current_user
from app.db import get_users_collection, get_products_collection, get_db
from app.scraper import fetch_product_data, get_asin_from_url
from app.services.product_service import update_prices
from app.config import AFFILIATE_TAG
from datetime import datetime
import logging
from app.services.analysis_service import analyze_product_price
from app.services.report_service import update_price_drops_report

router = APIRouter(prefix="/api", tags=["products"])
logger = logging.getLogger(__name__)

@router.post("/add-product/")
async def add_product(
    request: ProductRequest, 
    current_user: str = Depends(get_current_user), 
    users_collection = Depends(get_users_collection),
    products_collection = Depends(get_products_collection)
):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 1. Estrai ASIN dall'URL per controllare se esiste già nel DB globale
    asin = get_asin_from_url(request.product_url)
    
    if not asin:
        raise HTTPException(status_code=400, detail="Invalid Amazon URL (ASIN not found)")

    if any(product["asin"] == asin for product in db_user.get("products", [])):
        raise HTTPException(status_code=400, detail="Product already being tracked")

    # 2. Upsert global product
    global_product = products_collection.find_one({"asin": asin})
    
    if global_product:
        logger.info(f"Product {asin} already exists in global DB. Skipping initial scraping.")
        # Se il prodotto esiste già, lo usiamo senza fare scraping immediato
        # (Verrà aggiornato dallo scheduler o manualmente)
    else:
        logger.info(f"Product {asin} not found in global DB. Fetching data...")
        product_data = fetch_product_data(request.product_url)
        if not product_data or not product_data.get("price"):
            raise HTTPException(status_code=400, detail="Error fetching product data")
        
        initial_price = float(product_data["price"])
        product_data["max_price"] = initial_price
        product_data["min_price"] = initial_price
        product_data["average_price"] = initial_price
        product_data["price_history"] = [{"date": datetime.now().isoformat(), "price": initial_price}]
        products_collection.insert_one(product_data)
        global_product = product_data

    # 3. Add reference to user
    affiliate_link = f"https://www.amazon.it/gp/product/{asin}/?tag={AFFILIATE_TAG}"
    
    user_product_ref = {
        "asin": asin,
        "product_url": request.product_url,
        "category": request.category,
        "is_favorite": False,
        "added_at": datetime.now().isoformat()
    }

    users_collection.update_one(
        {"_id": db_user["_id"]},
        {"$push": {"products": user_product_ref}}
    )

    # Sync category to global product if missing
    if request.category:
        products_collection.update_one(
            {"asin": asin, "$or": [{"category": None}, {"category": ""}]},
            {"$set": {"category": request.category}}
        )
    
    return {"message": "Product added successfully", "affiliate": affiliate_link}

@router.get("/product-details/{asin}")
async def product_details(
    asin: str, 
    current_user: str = Depends(get_current_user), 
    users_collection = Depends(get_users_collection),
    products_collection = Depends(get_products_collection)
):
     db_user = users_collection.find_one({"username": current_user})
     if not db_user:
         raise HTTPException(status_code=404, detail="User not found")
         
     user_product = next((p for p in db_user.get("products", []) if p["asin"] == asin), None)
     if not user_product:
         raise HTTPException(status_code=404, detail="Product not found in user tracking")

     global_product = products_collection.find_one({"asin": asin})
     if not global_product:
         raise HTTPException(status_code=404, detail="Product global data not found")

     # Merge the data
     merged_product = {**global_product, **user_product}
     merged_product["affiliate"] = f"/api/analytics/r/{asin}"
     
     # Add AI Analysis
     merged_product["analysis"] = analyze_product_price(merged_product)

     # Rimuovi i campi _id per JSON serialization
     if "_id" in merged_product:
         del merged_product["_id"]
         
     return merged_product

@router.patch("/update-product-info/{asin}")
async def update_product_info(
    asin: str,
    updated_data: dict = Body(...),
    current_user: str = Depends(get_current_user),
    users_collection = Depends(get_users_collection)
):
    try:
        db_user = users_collection.find_one({"username": current_user})
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        products = db_user.get("products", [])
        product = next((p for p in products if p["asin"] == asin), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Update user-specific fields
        for key, value in updated_data.items():
            if key in ["category"]: # Solo i campi permessi per l'utente
                product[key] = value

        users_collection.update_one(
            {"_id": db_user["_id"], "products.asin": asin},
            {"$set": {f"products.$.{key}": value for key, value in updated_data.items()}}
        )

        # Sync category to global too
        if "category" in updated_data:
            get_products_collection(users_collection.database).update_one(
                {"asin": asin},
                {"$set": {"category": updated_data["category"]}}
            )

        return {"message": "Product updated successfully", "updated_product": product}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product info: {str(e)}")

@router.patch("/favorite/{asin}")
async def toggle_favorite(asin: str, current_user: str = Depends(get_current_user), users_collection = Depends(get_users_collection)):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    products = db_user.get("products", [])
    product = next((p for p in products if p["asin"] == asin), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_favorite_status = not product.get("is_favorite", False)
    users_collection.update_one(
        {"_id": db_user["_id"], "products.asin": asin},
        {"$set": {"products.$.is_favorite": new_favorite_status}}
    )

    return {"message": "Favorite status updated", "is_favorite": new_favorite_status}

@router.post("/update-prices-manual/")
async def update_prices_manual(current_user: str = Depends(get_current_user), users_collection = Depends(get_users_collection)):
    try:
        update_prices(users_collection, user_filter=current_user)
        # Update price drops report and send Telegram notifications
        update_price_drops_report()
        return {"message": "Price update triggered manually and report updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during manual price update")

@router.post("/update-selected-prices/")
async def update_selected_prices(
    asin_list: List[str],
    current_user: str = Depends(get_current_user),
    users_collection = Depends(get_users_collection)
):
    if not asin_list:
        raise HTTPException(status_code=400, detail="ASIN list cannot be empty")

    try:
        updated_products = update_prices(users_collection, user_filter=current_user, asin_filter=asin_list)
        return {"message": "Selected product prices updated", "updated_products": updated_products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating selected products: {str(e)}")

@router.post("/update-product/{asin}")
async def update_product_price(
    asin: str, 
    current_user: str = Depends(get_current_user), 
    users_collection = Depends(get_users_collection),
    products_collection = Depends(get_products_collection)
):
    try:
        updated_products = update_prices(users_collection, user_filter=current_user, asin_filter=[asin])

        if not updated_products:
            raise HTTPException(status_code=404, detail="Product not found or not updated")

        # Ritorna i dati aggiornati per questo utente
        db_user = users_collection.find_one({"username": current_user})
        user_product = next((p for p in db_user.get("products", []) if p["asin"] == asin), None)
        global_product = products_collection.find_one({"asin": asin})

        if not user_product or not global_product:
            raise HTTPException(status_code=404, detail="Product not found after update")

        merged = {**global_product, **user_product}

        return {
            "message": f"Product {asin} updated successfully",
            "product": {
                "asin": merged["asin"],
                "price": merged["price"],
                "price_history": merged.get("price_history", []),
                "max_price": merged.get("max_price"),
                "min_price": merged.get("min_price"),
                "average_price": merged.get("average_price"),
                "availability": merged.get("availability", "Unknown"),
                "condition": merged.get("condition", "Unknown"),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

@router.post("/remove-products/")
async def remove_products(asin_list: List[str], current_user: str = Depends(get_current_user), users_collection = Depends(get_users_collection)):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    result = users_collection.update_one(
        {"_id": db_user["_id"]},
        {"$pull": {"products": {"asin": {"$in": asin_list}}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No products were removed")

    return {"message": "Products removed successfully", "removed_asins": asin_list}

@router.delete("/remove-product/{asin}")
async def remove_product(asin: str, current_user: str = Depends(get_current_user), users_collection = Depends(get_users_collection)):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    result = users_collection.update_one(
        {"_id": db_user["_id"]},
        {"$pull": {"products": {"asin": asin}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product removed successfully"}

@router.get("/dashboard")
async def dashboard(
    current_user: str = Depends(get_current_user), 
    users_collection = Depends(get_users_collection),
    products_collection = Depends(get_products_collection)
):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_products = db_user.get("products", [])
    merged_products = []
    
    # Get all published articles to avoid N queries (optional but better)
    db = get_db()
    articles_cursor = db.articles.find({"asin": {"$in": [p.get("asin") for p in user_products if p.get("asin")]}})
    articles_map = {a["asin"]: a for a in articles_cursor}
    
    for user_product in user_products:
        asin = user_product.get("asin")
        if asin:
            global_product = products_collection.find_one({"asin": asin})
            if global_product:
                merged = {**global_product, **user_product}
                merged["affiliate"] = f"/api/analytics/r/{asin}"
                
                # Check for article
                article = articles_map.get(asin)
                if article:
                    merged["article_status"] = article.get("status")
                    merged["article_slug"] = article.get("slug")
                else:
                    merged["article_status"] = None
                    merged["article_slug"] = None

                # Add AI Analysis
                merged["analysis"] = analyze_product_price(merged)

                if "_id" in merged:
                    del merged["_id"]
                merged_products.append(merged)

    return {"products": merged_products}
