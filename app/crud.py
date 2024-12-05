# app/crud.py
from datetime import datetime
from app.db import users_collection
from app.scraper import fetch_product_data


def add_product_to_user(username, product_url):
    """Aggiunge un nuovo prodotto al database dell'utente con gestione completa dei prezzi."""
    # Esegui scraping del prodotto
    product_data = fetch_product_data(product_url)

    # Controlla se il prodotto è valido
    if not product_data or not product_data.get("price"):
        raise ValueError("Dati del prodotto non validi o prezzo non disponibile")

    # Trova l'utente nel database
    user = users_collection.find_one({"username": username})
    if not user:
        raise ValueError("Utente non trovato")

    # Verifica se il prodotto esiste già
    if any(p["asin"] == product_data["asin"] for p in user.get("products", [])):
        raise ValueError("Il prodotto è già monitorato")

    # Inizializza i dati dei prezzi per il prodotto
    initial_price = float(product_data["price"])
    product_data["max_price"] = initial_price
    product_data["min_price"] = initial_price
    product_data["average_price"] = initial_price
    product_data["price_history"] = [{"date": datetime.now().isoformat(), "price": initial_price}]

    # Aggiungi il prodotto alla lista dell'utente
    users_collection.update_one(
        {"username": username},
        {"$push": {"products": product_data}}
    )

    return {"message": "Prodotto aggiunto con successo"}


def get_price_history(username, asin):
    user = users_collection.find_one({"username": username})
    if not user:
        raise ValueError("Utente non trovato")

    # Cerca il prodotto con l'ASIN specificato
    product = next((p for p in user.get("products", []) if p["asin"] == asin), None)
    if not product:
        raise ValueError("Prodotto non trovato")

    return product["price_history"]

def get_user_products(username):
    user = users_collection.find_one({"username": username})
    if not user:
        raise ValueError("Utente non trovato")

    return user.get("products", [])

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




