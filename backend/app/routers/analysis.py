from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.db import get_users_collection, get_products_collection
from app.services.analysis_service import get_market_analysis
import logging

router = APIRouter(prefix="/api/analysis", tags=["analysis"])
logger = logging.getLogger(__name__)

@router.get("/")
async def get_analysis(
    current_user: str = Depends(get_current_user), 
    users_collection = Depends(get_users_collection),
    products_collection = Depends(get_products_collection)
):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user_products = db_user.get("products", [])
    
    if not user_products:
        return get_market_analysis([])

    # Recupera i dati globali per tutti questi ASIN
    asins = [p["asin"] for p in user_products]
    global_products = list(products_collection.find({"asin": {"$in": asins}}))

    # Facciamo un merge dei dati dell'utente (come categoria e preferiti) con i dati globali
    merged_products = []
    for user_prod in user_products:
        global_prod = next((p for p in global_products if p["asin"] == user_prod["asin"]), None)
        if global_prod:
            merged_products.append({**global_prod, **user_prod})
            
    analysis_data = get_market_analysis(merged_products)
    
    return analysis_data
