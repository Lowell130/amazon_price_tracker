# app/crud.py
from datetime import datetime
from app.db import users_collection, products_collection
from app.scraper import fetch_product_data


def add_product_to_user(username, product_url):
    """Aggiunge un nuovo prodotto al database globale e il riferimento all'utente."""
    # Recupera modalità scraper dai settings
    settings_collection = users_collection.database["settings"]
    settings = settings_collection.find_one({"type": "scraper_config"})
    scraper_mode = settings.get("mode", "classic") if settings else "classic"
    
    # Esegui scraping del prodotto
    product_data = fetch_product_data(product_url, mode=scraper_mode)

    # Controlla se il prodotto è valido
    if not product_data or not product_data.get("price"):
        raise ValueError("Dati del prodotto non validi o prezzo non disponibile")

    asin = product_data["asin"]

    # Trova l'utente nel database
    user = users_collection.find_one({"username": username})
    if not user:
        raise ValueError("Utente non trovato")

    # Verifica se l'utente ha già questo prodotto
    if any(p["asin"] == asin for p in user.get("products", [])):
        raise ValueError("Il prodotto è già monitorato da questo utente")

    # Controlla se il prodotto esiste già a livello globale
    global_product = products_collection.find_one({"asin": asin})

    if not global_product:
        # Inizializza i dati del prodotto globale
        initial_price = float(product_data["price"])
        product_data["max_price"] = initial_price
        product_data["min_price"] = initial_price
        product_data["average_price"] = initial_price
        product_data["price_history"] = [{"date": datetime.now().isoformat(), "price": initial_price}]
        
        # Inserisci il prodotto globale
        products_collection.insert_one(product_data)
    else:
        # Potremmo voler aggiornare il prezzo qui, ma per ora ci affidiamo al global_product esistente
        pass

    # Prepara il riferimento base da salvare per l'utente
    user_product_ref = {
        "asin": asin,
        "product_url": product_url,
        "is_favorite": False,
        "added_at": datetime.now().isoformat()
    }

    # Aggiungi il riferimento alla lista dell'utente
    users_collection.update_one(
        {"username": username},
        {"$push": {"products": user_product_ref}}
    )

    return {"message": "Prodotto aggiunto con successo globale e aggiunto all'utente"}

def get_price_history(username, asin):
    # Cerca il prodotto globalmente
    product = products_collection.find_one({"asin": asin})
    if not product:
        raise ValueError("Prodotto non trovato")

    return product.get("price_history", [])

def remove_product_from_user(username, asin):
    user = users_collection.find_one({"username": username})
    if not user:
        raise ValueError("Utente non trovato")

    # Rimuovi il prodotto dall'elenco
    users_collection.update_one(
        {"username": username},
        {"$pull": {"products": {"asin": asin}}}
    )
    return {"message": "Prodotto eliminato con successo"}


def calculate_average(prices):
    """Calcola la media dei prezzi."""
    return sum(prices) / len(prices) if prices else None

def update_product_prices(product, new_price):
    """Aggiorna i dati di prezzo di un prodotto."""
    price_history = product.get("price_history", [])
    # Aggiungi il nuovo prezzo alla cronologia
    price_history.append({"date": datetime.now().isoformat(), "price": new_price})
    all_prices = [entry["price"] for entry in price_history]

    # Aggiorna i dati relativi ai prezzi
    product["price"] = new_price
    product["price_history"] = price_history
    product["max_price"] = max(all_prices)
    product["min_price"] = min(all_prices)
    product["average_price"] = calculate_average(all_prices)




