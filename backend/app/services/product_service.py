from app.scraper import fetch_product_data
from app.utils.email import send_email
from app.db import get_products_collection, get_users_collection
from datetime import datetime
import logging

# Configura il logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def update_prices(users_collection, user_filter=None, asin_filter=None):
    products_collection = get_products_collection()
    settings_collection = users_collection.database["settings"]
    
    # Recupera modalità scraper
    settings = settings_collection.find_one({"type": "scraper_config"})
    scraper_mode = settings.get("mode", "classic") if settings else "classic"
    logger.info(f"Using scraper mode: {scraper_mode}")
    
    # 1. Determina gli ASIN da aggiornare
    asins_to_update = set()
    
    if user_filter:
        user = users_collection.find_one({"username": user_filter})
        if user:
            user_asins = {p["asin"] for p in user.get("products", [])}
            if asin_filter:
                asins_to_update.update(user_asins.intersection(set(asin_filter)))
            else:
                asins_to_update.update(user_asins)
    elif asin_filter:
        asins_to_update.update(set(asin_filter))
    else:
        # Nessun filtro: aggiorna tutti i prodotti nel database globale
        all_products = products_collection.find({}, {"asin": 1})
        asins_to_update.update({p["asin"] for p in all_products})

    logger.info(f"Starting price update for {len(asins_to_update)} ASINs")

    updated_products = []

    for asin in asins_to_update:
        global_product = products_collection.find_one({"asin": asin})
        if not global_product:
            logger.warning(f"ASIN {asin} not found in global products database")
            continue
        
        # Recuperiamo un URL base da cui fare scraping. 
        # Troviamo il primo utente che ha l'URL originale oppure usiamo un link base.
        # È più sicuro usare il link dal db utente che lo ha tracciato
        product_url = None
        user_tracking = users_collection.find_one({"products.asin": asin})
        if user_tracking:
            user_product = next((p for p in user_tracking.get("products", []) if p["asin"] == asin), None)
            if user_product:
                product_url = user_product.get("product_url")
        
        if not product_url:
            product_url = f"https://www.amazon.it/dp/{asin}"

        try:
            logger.info(f"Fetching product data for ASIN: {asin} (Mode: {scraper_mode})")
            updated_data = fetch_product_data(product_url, mode=scraper_mode)

            if not updated_data or updated_data["price"] is None:
                logger.info(f"Product {asin} price not found. Keeping last known price.")
                products_collection.update_one(
                    {"asin": asin},
                    {"$set": {"availability": "Dato non aggiornato", "updated_at": datetime.now()}}
                )
                updated_products.append(asin)
                continue

            old_price = float(global_product.get("price")) if global_product.get("price") else None
            new_price = float(updated_data["price"])
            price_dropped = old_price and new_price < old_price

            # Check for interested users
            interested_users = users_collection.find({"products.asin": asin})
            for u in interested_users:
                u_prod = next((p for p in u.get("products", []) if p["asin"] == asin), None)
                if not u_prod:
                    continue
                
                # Check favorite drop
                if u_prod.get("is_favorite", False) and price_dropped:
                    subject = f"📉 Calo Prezzo: {global_product.get('title', 'Prodotto Amazon')[:50]}..."
                    body = (
                        f"Il prezzo di '{global_product.get('title')}' è sceso!\n\n"
                        f"Prezzo Precedente: {old_price}€\n"
                        f"Nuovo Prezzo: {new_price}€\n\n"
                        f"Vedi l'offerta su Amazon: {u_prod.get('affiliate', product_url)}"
                    )
                    send_email(u.get("email"), subject, body)
                    
                    # Notifica Telegram se configurato
                    if u.get("telegram_chat_id"):
                        try:
                            from app.config import TEL_TOKEN
                            if TEL_TOKEN:
                                import requests
                                message = (
                                    f"📉 *{global_product.get('title', 'Prodotto')}*\n"
                                    f"🔻 *Prezzo:* {new_price}€ (era {old_price}€)\n"
                                    f"🔗 [Link Amazon]({u_prod.get('affiliate', product_url)})"
                                )
                                requests.post(
                                    f"https://api.telegram.org/bot{TEL_TOKEN}/sendMessage",
                                    data={
                                        "chat_id": u["telegram_chat_id"],
                                        "text": message,
                                        "parse_mode": "Markdown",
                                        "disable_web_page_preview": True
                                    },
                                    timeout=10
                                )
                                logger.info(f"Telegram notification sent to {u['username']}")
                        except Exception as e:
                            logger.error(f"Error sending Telegram notification: {e}")

            # Aggiornamento dello storico e dei campi del prodotto globale
            price_history = global_product.get("price_history", [])
            price_history.append({"date": datetime.now().isoformat(), "price": new_price})
            
            max_price_entry = max(price_history, key=lambda x: float(x["price"]))
            min_price_entry = min(price_history, key=lambda x: float(x["price"]))
            
            update_fields = {
                "price": new_price,
                "price_history": price_history,
                "availability": "Disponibile",
                "condition": updated_data.get("condition"),
                "coupon": updated_data.get("coupon", False),
                "coupon_value": updated_data.get("coupon_value"),
                "max_price": float(max_price_entry["price"]),
                "min_price": float(min_price_entry["price"]),
                "average_price": round(sum(float(entry["price"]) for entry in price_history) / len(price_history), 2)
            }
            
            products_collection.update_one({"asin": asin}, {"$set": update_fields})
            updated_products.append(asin)
            logger.info(f"Updated product {asin} globally - New Price: {new_price} €")

        except Exception as e:
            logger.error(f"Error updating product {asin}: {e}")
            continue

    logger.info("Finished updating products.")
    return updated_products
