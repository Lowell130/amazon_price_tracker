from app.scraper import fetch_product_data, ScraperBlockedException
from app.utils.email import send_email
from app.db import get_products_collection, get_users_collection
from datetime import datetime
import os
import logging

# Configura il logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def update_prices(users_collection, user_filter=None, asin_filter=None):
    products_collection = get_products_collection()
    settings_collection = users_collection.database["settings"]
    
    # Determina se si tratta di un aggiornamento globale (senza filtri)
    is_global_update = not user_filter and not asin_filter
    
    # Recupera configurazioni
    settings = settings_collection.find_one({"type": "scraper_config"})
    scraper_mode = settings.get("mode", "classic") if settings else "classic"
    max_retries = settings.get("max_retries", 3) if settings else 3
    
    from app.config import AFFILIATE_TAG
    current_tag = settings.get("affiliate_tag", AFFILIATE_TAG) if settings else AFFILIATE_TAG
    
    logger.info(f"Using scraper mode: {scraper_mode} (Max retries: {max_retries})")
    
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
    blocked_asins = []
    failed_asins = []
    
    # Raggruppa le email da inviare agli utenti alla fine del processo
    user_email_drops = {}

    start_time = datetime.now()

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
            updated_data = fetch_product_data(product_url, mode=scraper_mode, max_retries=max_retries)

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
                    # Costruisci l'URL finale con tag di affiliazione
                    final_affiliate_url = u_prod.get('affiliate')
                    if not final_affiliate_url:
                        # Se non c'è un link specifico, costruisci quello base con il tag corrente
                        connector = "&" if "?" in product_url else "?"
                        final_affiliate_url = f"{product_url}{connector}tag={current_tag}"
                    
                    # Salva il calo di prezzo nel dizionario per inviarlo dopo in un'unica email
                    user_email = u.get("email")
                    if user_email:
                        if user_email not in user_email_drops:
                            user_email_drops[user_email] = []
                        user_email_drops[user_email].append({
                            "title": global_product.get('title', 'Prodotto Amazon'),
                            "old_price": old_price,
                            "new_price": new_price,
                            "url": final_affiliate_url
                        })
                    
                    # Notifica Telegram se configurato
                    if u.get("telegram_chat_id"):
                        try:
                            from app.config import TEL_TOKEN
                            if TEL_TOKEN:
                                import requests
                                message = (
                                    f"📉 *{global_product.get('title', 'Prodotto')}*\n"
                                    f"🔻 *Prezzo:* {new_price}€ (era {old_price}€)\n"
                                    f"🔗 [Link Amazon]({final_affiliate_url})"
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
            
            # Manteniamo solo gli ultimi 60 prezzi (circa 1 mese se aggiornato 2 volte al giorno) per evitare esplosione dello storage
            if len(price_history) > 60:
                price_history = price_history[-60:]
            
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
                "average_price": round(sum(float(entry["price"]) for entry in price_history) / len(price_history), 2),
                "extraction_date": datetime.now().isoformat()
            }
            
            products_collection.update_one({"asin": asin}, {"$set": update_fields})
            updated_products.append(asin)
            logger.info(f"Updated product {asin} globally - New Price: {new_price} €")

        except ScraperBlockedException as e:
            logger.warning(f"Product {asin} blocked by Amazon: {e}")
            blocked_asins.append(asin)
            products_collection.update_one(
                {"asin": asin},
                {"$set": {"availability": "Bloccato da Amazon", "updated_at": datetime.now()}}
            )
            continue
        except Exception as e:
            logger.error(f"Error updating product {asin}: {e}")
            failed_asins.append(asin)
            continue

    end_time = datetime.now()
    duration = end_time - start_time
    
    # Invia le email raggruppate agli utenti per i cali di prezzo preferiti
    for user_email, drops in user_email_drops.items():
        if not drops:
            continue
        subject = f"📉 Report Cali di Prezzo - {len(drops)} prodotti aggiornati"
        body = "Ecco i cali di prezzo registrati per i tuoi prodotti preferiti:\n\n"
        for drop in drops:
            body += (
                f"🔸 {drop['title']}\n"
                f"   Prezzo Precedente: {drop['old_price']}€\n"
                f"   Nuovo Prezzo: {drop['new_price']}€\n"
                f"   Vedi l'offerta: {drop['url']}\n\n"
            )
        try:
            send_email(user_email, subject, body)
            logger.info(f"Grouped price drop email sent to {user_email} with {len(drops)} items.")
        except Exception as e:
            logger.error(f"Failed to send grouped price drop email to {user_email}: {e}")

    # Invia report all'admin
    admin_email = settings.get("admin_report_email") if settings else None
    if not admin_email:
        admin_email = os.getenv("SENDER_EMAIL")
    
    if is_global_update and admin_email:
        subject = f"📊 Report Aggiornamento Prezzi - {end_time.strftime('%d/%m/%Y %H:%M')}"
        body = (
            f"Il job di aggiornamento prezzi è terminato.\n\n"
            f"Riepilogo:\n"
            f"-----------------------------------\n"
            f"Totale prodotti: {len(asins_to_update)}\n"
            f"Aggiornati con successo: {len(updated_products)}\n"
            f"Bloccati da Amazon (saltati): {len(blocked_asins)}\n"
            f"Falliti (errori tecnici): {len(failed_asins)}\n"
            f"Durata: {duration}\n"
            f"-----------------------------------\n\n"
            f"Dettagli prodotti bloccati:\n"
            f"{', '.join(blocked_asins) if blocked_asins else 'Nessuno'}\n\n"
            f"Dettagli errori tecnici:\n"
            f"{', '.join(failed_asins) if failed_asins else 'Nessuno'}"
        )
        try:
            send_email(admin_email, subject, body)
            logger.info(f"Admin report email sent to {admin_email}")
        except Exception as e:
            logger.error(f"Failed to send admin report email: {e}")

    logger.info("Finished updating products.")
    return updated_products
