from datetime import datetime
from app.db import get_db
from app.telegram_bot import broadcast_price_drops
import logging

logger = logging.getLogger(__name__)

def update_price_drops_report():
    """Analisi globale dei cali di prezzo per Home Page e Telegram Channel."""
    try:
        db = get_db()
        products_collection = db["products"]
        price_drops_collection = db["price_drops"]
        
        # Svuota report precedente (manteniamo solo l'ultima versione)
        price_drops_collection.delete_many({})
        
        report = {
            "generation_date": datetime.now().isoformat(),
            "drops": []
        }
        
        # Trova prodotti con calo di prezzo confrontando gli ultimi due inserimenti nello storico
        products = list(products_collection.find({}))
        
        for product in products:
            price_history = product.get("price_history", [])
            if len(price_history) < 2:
                continue
            
            # Assicurati che lo storico sia ordinato cronologicamente
            price_history = sorted(price_history, key=lambda x: x["date"])
            
            old_price = float(price_history[-2]["price"])
            new_price = float(price_history[-1]["price"])
            
            # Se il prezzo è sceso
            if new_price < old_price:
                # Prepara il dato del drop includendo informazioni utili al frontend
                drop_info = {
                    "asin": product["asin"],
                    "title": product["title"],
                    "old_price": old_price,
                    "new_price": new_price,
                    "price_drop": round(old_price - new_price, 2),
                    "category": product.get("category", "Uncategorized"),
                    "date": price_history[-1]["date"],
                    "image_url": product.get("image_url", ""),
                    "rating": product.get("rating"),
                    "availability": product.get("availability", "Disponibile"),
                    "condition": product.get("condition", "Nuovo"),
                    "coupon": product.get("coupon", False),
                    "coupon_value": product.get("coupon_value"),
                }
                report["drops"].append(drop_info)
        
        # Se abbiamo trovato dei cali, salviamo il report e inviamo a Telegram
        if report["drops"]:
            # Ordina i drop per entità dello sconto (opzionale, utile per la Home Page)
            report["drops"].sort(key=lambda x: x["price_drop"], reverse=True)
            
            price_drops_collection.insert_one(report)
            logger.info(f"Report cali di prezzo generato con {len(report['drops'])} prodotti.")
            
            # Broadcast al canale Telegram (legge l'ultimo report appena inserito)
            try:
                broadcast_price_drops()
                logger.info("Broadcast Telegram completato con successo.")
            except Exception as te:
                logger.error(f"Errore durante il broadcast Telegram: {te}")
        else:
            logger.info("Nessun calo di prezzo rilevato, report non generato.")
            
        return len(report["drops"])
        
    except Exception as e:
        logger.error(f"Errore critico durante update_price_drops_report: {e}")
        return 0
