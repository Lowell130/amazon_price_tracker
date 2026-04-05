from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import admin_required, password_reset_tokens, generate_reset_token
from app.db import get_users_collection, get_db, get_settings_collection
from app.schemas import ScraperSettings
from app.services.product_service import update_prices
from app.utils.email import send_email
from datetime import datetime, timedelta
import os
import subprocess
import logging
from app.telegram_bot import broadcast_price_drops
from app.services.report_service import update_price_drops_report

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(admin_required)])
logger = logging.getLogger(__name__)

@router.get("/users")
async def get_all_users(users_collection = Depends(get_users_collection)):
    users_cursor = users_collection.find({})
    users_list = []
    for user in users_cursor:
        users_list.append({
            "username": user["username"],
            "email": user.get("email"),
            "admin": user.get("admin", False),
            "products_count": len(user.get("products", []))
        })
    return users_list

@router.delete("/users/{username}")
async def delete_user(username: str, users_collection = Depends(get_users_collection)):
    result = users_collection.delete_one({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {username} deleted successfully"}

@router.patch("/users/{username}/toggle-admin")
async def toggle_admin(username: str, users_collection = Depends(get_users_collection)):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_status = not user.get("admin", False)
    users_collection.update_one({"username": username}, {"$set": {"admin": new_status}})
    return {"message": f"Admin status for {username} set to {new_status}", "admin": new_status}

@router.get("/users/{username}/products")
async def get_user_products(username: str, users_collection = Depends(get_users_collection)):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_products = user.get("products", [])
    products_collection = users_collection.database["products"]
    
    merged_products = []
    for user_prod in user_products:
        asin = user_prod.get("asin")
        global_prod = products_collection.find_one({"asin": asin})
        if global_prod:
            # Merge: global data + user specific data (category, favorite status etc)
            merged = {**global_prod, **user_prod}
            if "_id" in merged:
                del merged["_id"]
            merged_products.append(merged)
            
    return merged_products

@router.post("/users/{username}/reset-password")
async def admin_reset_password(username: str, users_collection = Depends(get_users_collection)):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    email = user.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="User has no email address")

    # Generate reset token
    reset_token = generate_reset_token()
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    password_reset_tokens[reset_token] = {"email": email, "expires_at": expiration_time}

    # Construct reset link
    frontend_base_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:8080")
    reset_link = f"{frontend_base_url}/reset-password?token={reset_token}"

    # Send email
    send_email(
        email,
        "Password Reset Request (Admin)",
        f"Un amministratore ha richiesto il reset della tua password.\n"
        f"Usa il seguente link per reimpostare la tua password: {reset_link}\n"
        f"Il link scade in un'ora."
    )

    return {"message": f"Password reset email sent to {email}"}

@router.post("/generate-price-drops-report")
async def generate_price_drops_report():
    """Genera manualmente il report dei cali di prezzo (per admin)."""
    try:
        total_drops = update_price_drops_report()
        return {
            "message": f"Price drops report generated and broadcast to Telegram",
            "total_price_drops": total_drops,
        }
    except Exception as e:
        logger.error(f"Error generating report manually: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@router.post("/update-all-prices")
async def update_all_prices_manual(users_collection = Depends(get_users_collection)):
    """Aggiorna manualmente i prezzi di **tutti** i prodotti nel database."""
    try:
        updated_products = update_prices(users_collection, user_filter=None)  
        # Update price drops report and send Telegram notifications
        update_price_drops_report()
        return {
            "message": "Manual price update for all products completed and report updated",
            "updated_products_count": len(updated_products),
        }
    except Exception as e:
        logger.error(f"Error updating all prices manually: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during manual price update: {str(e)}")

@router.get("/settings", response_model=ScraperSettings)
async def get_system_settings(settings_collection = Depends(get_settings_collection)):
    """Recupera le impostazioni di sistema (es. modalità scraper, proxy)."""
    settings = settings_collection.find_one({"type": "scraper_config"})
    if not settings:
        return ScraperSettings(mode="classic", use_proxy=False)
    
    from app.config import AFFILIATE_TAG
    return ScraperSettings(
        mode=settings.get("mode", "classic"),
        use_proxy=settings.get("use_proxy", False),
        proxy_url=settings.get("proxy_url"),
        proxy_user=settings.get("proxy_user"),
        proxy_pass=settings.get("proxy_pass"),
        auto_refresh=settings.get("auto_refresh", True),
        auto_update_prices=settings.get("auto_update_prices", True),
        affiliate_tag=settings.get("affiliate_tag", AFFILIATE_TAG)
    )

@router.post("/settings")
async def update_system_settings(settings: ScraperSettings, settings_collection = Depends(get_settings_collection)):
    """Aggiorna le impostazioni di sistema."""
    update_data = {
        "mode": settings.mode,
        "use_proxy": settings.use_proxy,
        "proxy_url": settings.proxy_url,
        "proxy_user": settings.proxy_user,
        "proxy_pass": settings.proxy_pass,
        "auto_refresh": settings.auto_refresh,
        "auto_update_prices": settings.auto_update_prices,
        "affiliate_tag": settings.affiliate_tag,
        "updated_at": datetime.now()
    }
    
    settings_collection.update_one(
        {"type": "scraper_config"},
        {"$set": update_data},
        upsert=True
    )
    return {"message": "System settings updated successfully"}
