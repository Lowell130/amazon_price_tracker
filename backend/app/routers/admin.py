from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import admin_required, password_reset_tokens, generate_reset_token
from app.db import users_collection
from app.services.product_service import update_prices
from app.utils.email import send_email
from datetime import datetime, timedelta
import os
import subprocess
import logging

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(admin_required)])
logger = logging.getLogger(__name__)

@router.get("/users")
async def get_all_users():
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
async def delete_user(username: str):
    result = users_collection.delete_one({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {username} deleted successfully"}

@router.patch("/users/{username}/toggle-admin")
async def toggle_admin(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_status = not user.get("admin", False)
    users_collection.update_one({"username": username}, {"$set": {"admin": new_status}})
    return {"message": f"Admin status for {username} set to {new_status}", "admin": new_status}

@router.get("/users/{username}/products")
async def get_user_products(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.get("products", [])

@router.post("/users/{username}/reset-password")
async def admin_reset_password(username: str):
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
    try:
        price_drops_collection = users_collection.database["price_drops"]
        price_drops_collection.delete_many({})

        users = users_collection.find({})
        report = {
            "generation_date": datetime.now().isoformat(),
            "drops": []
        }

        for user in users:
            for product in user.get("products", []):
                price_history = product.get("price_history", [])
                if len(price_history) < 2:
                    continue

                price_history = sorted(price_history, key=lambda x: x["date"])
                old_price = price_history[-2]["price"]
                new_price = price_history[-1]["price"]

                if new_price < old_price:
                    report["drops"].append({
                        "asin": product["asin"],
                        "title": product["title"],
                        "old_price": old_price,
                        "new_price": new_price,
                        "price_drop": round(old_price - new_price, 2),
                        "user": user["username"],
                        "category": product.get("category"),
                        "date": price_history[-1]["date"],
                        "affiliate": product.get("affiliate"),
                        "condition": product.get("condition", "Unknown"),
                        "image_url": product.get("image_url", ""),
                        "rating": product.get("rating", None),
                        "availability": product.get("availability", "Unknown"),
                        "insertion_date": product.get("insertion_date", None),
                    })

        price_drops_collection.insert_one(report)

        # Start Telegram bot
        subprocess.Popen(["python", "app/telegram_bot.py"])

        return {
            "message": "Price drops report generated and Telegram bot started",
            "total_price_drops": len(report["drops"]),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@router.post("/update-all-prices")
async def update_all_prices_manual():
    """Aggiorna manualmente i prezzi di **tutti** i prodotti nel database."""
    try:
        updated_products = update_prices(user_filter=None)  
        return {
            "message": "Manual price update for all products completed",
            "updated_products_count": len(updated_products),
        }
    except Exception as e:
        logger.error(f"Error updating all prices manually: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during manual price update: {str(e)}")
