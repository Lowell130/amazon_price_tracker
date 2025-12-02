from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import List
from app.schemas import ProductRequest
from app.dependencies import get_current_user
from app.db import users_collection
from app.scraper import fetch_product_data
from app.services.product_service import update_prices
from app.config import AFFILIATE_TAG
import logging

router = APIRouter(prefix="/api", tags=["products"])
logger = logging.getLogger(__name__)

@router.post("/add-product/")
async def add_product(request: ProductRequest, current_user: str = Depends(get_current_user)):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    product_data = fetch_product_data(request.product_url)
    if not product_data or not product_data.get("price"):
        raise HTTPException(status_code=400, detail="Error fetching product data")

    asin = product_data["asin"]

    if any(product["asin"] == asin for product in db_user.get("products", [])):
        raise HTTPException(status_code=400, detail="Product already being tracked")

    affiliate_link = f"https://www.amazon.it/gp/product/{asin}/?tag={AFFILIATE_TAG}"

    product_data.update({
        "product_url": request.product_url,
        "category": request.category,
        "affiliate": affiliate_link,
    })

    users_collection.update_one(
        {"_id": db_user["_id"]},
        {"$push": {"products": product_data}}
    )
    return {"message": "Product added successfully", "affiliate": affiliate_link}

@router.get("/product-details/{asin}")
async def product_details(asin: str, current_user: str = Depends(get_current_user)):
     db_user = users_collection.find_one({"username": current_user})
     if not db_user:
         raise HTTPException(status_code=404, detail="User not found")
     product = next((p for p in db_user.get("products", []) if p["asin"] == asin), None)
     if not product:
         raise HTTPException(status_code=404, detail="Product not found")

     return product

@router.patch("/update-product-info/{asin}")
async def update_product_info(
    asin: str,
    updated_data: dict = Body(...),
    current_user: str = Depends(get_current_user)
):
    try:
        db_user = users_collection.find_one({"username": current_user})
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        products = db_user.get("products", [])
        product = next((p for p in products if p["asin"] == asin), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        for key, value in updated_data.items():
            if key in product:
                product[key] = value

        users_collection.update_one(
            {"_id": db_user["_id"], "products.asin": asin},
            {"$set": {f"products.$.{key}": value for key, value in updated_data.items()}}
        )

        return {"message": "Product updated successfully", "updated_product": product}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product info: {str(e)}")

@router.patch("/favorite/{asin}")
async def toggle_favorite(asin: str, current_user: str = Depends(get_current_user)):
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
async def update_prices_manual(current_user: str = Depends(get_current_user)):
    """Aggiorna manualmente i prezzi dei prodotti per l'utente corrente."""
    try:
        update_prices(user_filter=current_user)
        return {"message": "Price update triggered manually"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during manual price update")

@router.post("/update-selected-prices/")
async def update_selected_prices(
    asin_list: List[str],
    current_user: str = Depends(get_current_user)
):
    if not asin_list:
        raise HTTPException(status_code=400, detail="ASIN list cannot be empty")

    try:
        updated_products = update_prices(user_filter=current_user, asin_filter=asin_list)
        return {"message": "Selected product prices updated", "updated_products": updated_products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating selected products: {str(e)}")

@router.post("/update-product/{asin}")
async def update_product_price(asin: str, current_user: str = Depends(get_current_user)):
    try:
        updated_products = update_prices(user_filter=current_user, asin_filter=[asin])

        if not updated_products:
            raise HTTPException(status_code=404, detail="Product not found or not updated")

        db_user = users_collection.find_one({"username": current_user})
        product = next((p for p in db_user.get("products", []) if p["asin"] == asin), None)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found after update")

        return {
            "message": f"Product {asin} updated successfully",
            "product": {
                "asin": product["asin"],
                "price": product["price"],
                "price_history": product["price_history"],
                "max_price": product["max_price"],
                "min_price": product["min_price"],
                "average_price": product["average_price"],
                "availability": product.get("availability", "Unknown"),
                "condition": product.get("condition", "Unknown"),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

@router.post("/remove-products/")
async def remove_products(asin_list: List[str], current_user: str = Depends(get_current_user)):
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
async def remove_product(asin: str, current_user: str = Depends(get_current_user)):
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
async def dashboard(current_user: str = Depends(get_current_user)):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"products": db_user.get("products", [])}
