from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.db import get_users_collection
from app.services.analysis_service import get_market_analysis
import logging

router = APIRouter(prefix="/api/analysis", tags=["analysis"])
logger = logging.getLogger(__name__)

@router.get("/")
async def get_analysis(current_user: str = Depends(get_current_user), users_collection = Depends(get_users_collection)):
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    products = db_user.get("products", [])
    analysis_data = get_market_analysis(products)
    
    return analysis_data
