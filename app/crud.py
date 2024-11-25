# app/crud.py
from datetime import datetime
from app.db import users_collection
from app.scraper import fetch_product_data

def add_product_to_user(username, product_url):
    # Recupera i dati del prodotto tramite scraping
    product_data = fetch_product_data(product_url)
    product_data["product_url"] = product_url
    product_data["insertion_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    product_data["price_history"] = [{"date": product_data["extraction_date"], "price": product_data["price"]}]

    # Verifica se l'utente esiste
    user = users_collection.find_one({"username": username})
    if not user:
        raise ValueError("Utente non trovato")

    # Controlla se il prodotto esiste già
    if any(p["asin"] == product_data["asin"] for p in user.get("products", [])):
        raise ValueError("Il prodotto è già monitorato")

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
