# app/crud.py
import json
import os
from app.scraper import fetch_product_data

USER_DATA_DIR = "data/users"

def add_product_to_user(username, product_url):
    """Aggiunge un prodotto al file JSON dell'utente."""
    user_file = f"{USER_DATA_DIR}/{username}.json"
    if not os.path.exists(user_file):
        raise ValueError("Utente non trovato")

    # Recupera i dati del prodotto tramite scraping
    product_data = fetch_product_data(product_url)
    
    # Aggiunge il nuovo prodotto o aggiorna se già esiste
    with open(user_file, "r+") as f:
        user_data = json.load(f)
        products = user_data.get("products", [])
        
        # Controlliamo se il prodotto esiste già
        existing_product = next((p for p in products if p["asin"] == product_data["asin"]), None)
        if existing_product:
            raise ValueError("Il prodotto è già monitorato")

        # Aggiungiamo il prodotto con lo storico dei prezzi
        product_data["price_history"] = [{"date": product_data["extraction_date"], "price": product_data["price"]}]
        products.append(product_data)
        user_data["products"] = products
        f.seek(0)
        json.dump(user_data, f, indent=4)
        f.truncate()

    return {"message": "Prodotto aggiunto con successo"}


# app/crud.py (aggiunta)
def get_price_history(username, asin):
    """Recupera lo storico prezzi di un prodotto dato l'ASIN."""
    user_file = f"{USER_DATA_DIR}/{username}.json"
    if not os.path.exists(user_file):
        raise ValueError("Utente non trovato")

    with open(user_file, "r") as f:
        user_data = json.load(f)
        product = next((p for p in user_data["products"] if p["asin"] == asin), None)
        if not product:
            raise ValueError("Prodotto non trovato")

        return product["price_history"]

