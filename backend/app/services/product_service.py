from app.db import users_collection
from app.scraper import fetch_product_data
from app.utils.email import send_email
from datetime import datetime
import logging

# Configura il logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def update_prices(user_filter=None, asin_filter=None):
    query = {"username": user_filter} if user_filter else {}
    users = users_collection.find(query)
    updated_products = []

    for user in users:
        email = user.get("email")  # Assumiamo che l'email sia salvata nel profilo utente
        products = user.get("products", [])
        logger.info(f"Updating prices for user: {user['username']} ({len(products)} products)")

        for product in products:
            if asin_filter and product["asin"] not in asin_filter:
                continue

            try:
                logger.info(f"Fetching product data for ASIN: {product['asin']}")
                updated_data = fetch_product_data(product["product_url"])

                if not updated_data or updated_data["price"] is None:
                    product["availability"] = "Non disponibile"
                    product["condition"] = "Non disponibile"
                    logger.info(f"Product {product['asin']} is unavailable.")
                    continue

                old_price = float(product["price"]) if product["price"] else None
                new_price = float(updated_data["price"])

                if product.get("is_favorite", False) and old_price and new_price < old_price:
                    logger.info(f"Price drop detected for {product['title']}. Sending email.")
                    send_email(email, product["title"], old_price, new_price, product["asin"])


                product["price_history"].append({"date": datetime.now().isoformat(), "price": new_price})
                product["price"] = new_price
                product["availability"] = "Disponibile"
                product["condition"] = updated_data["condition"]

                # ✅ AGGIUNTA QUI: salva le info del coupon
                product["coupon"] = updated_data.get("coupon", False)
                product["coupon_value"] = updated_data.get("coupon_value")

                # Calcola max, min, e average price
                price_history = product["price_history"]
                max_price_entry = max(price_history, key=lambda x: float(x["price"]))
                min_price_entry = min(price_history, key=lambda x: float(x["price"]))

                product["max_price"] = float(max_price_entry["price"])
                product["min_price"] = float(min_price_entry["price"])
                product["average_price"] = round(
                    sum(float(entry["price"]) for entry in price_history) / len(price_history), 2
                )

                updated_products.append(product["asin"])
                logger.info(f"Updated product {product['asin']} - New Price: {new_price} €")

            except Exception as e:
                logger.error(f"Error updating product {product['asin']}: {e}")
                continue

        users_collection.update_one({"_id": user["_id"]}, {"$set": {"products": products}})
        logger.info(f"Finished updating products for user: {user['username']}")

    return updated_products
