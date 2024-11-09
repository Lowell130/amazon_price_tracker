# app/crud.py
import json
import os
from app.scraper import fetch_product_data
from datetime import datetime

USER_DATA_DIR = "data/users"

# Funzione per aggiungere un prodotto al file JSON dell'utente
# Funzione per aggiungere un prodotto al file JSON dell'utente
def add_product_to_user(username, product_url):
    user_file = f"{USER_DATA_DIR}/{username}.json"
    if not os.path.exists(user_file):
        raise ValueError("Utente non trovato")

    # Recupera i dati del prodotto tramite scraping
    product_data = fetch_product_data(product_url)
    
    # Aggiungi `product_url` e `insertion_date`
    product_data["product_url"] = product_url  # Salva l'URL originale
    product_data["insertion_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Data di inserimento

    # Aggiunge il nuovo prodotto o verifica se già esiste
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


# Funzione per ottenere la cronologia dei prezzi di un prodotto
def get_price_history(username, asin):
    user_file = f"{USER_DATA_DIR}/{username}.json"
    if not os.path.exists(user_file):
        raise ValueError("Utente non trovato")

    with open(user_file, "r") as f:
        user_data = json.load(f)
        product = next((p for p in user_data["products"] if p["asin"] == asin), None)
        if not product:
            raise ValueError("Prodotto non trovato")

        return product["price_history"]

# Funzione per ottenere tutti i prodotti monitorati di un utente
def get_user_products(username):
    user_file = f"{USER_DATA_DIR}/{username}.json"
    if not os.path.exists(user_file):
        raise ValueError("Utente non trovato")

    with open(user_file, "r") as f:
        user_data = json.load(f)
        return user_data.get("products", [])

# Funzione per rimuovere un prodotto dal file JSON dell'utente
def remove_product_from_user(username, asin):
    user_file = f"{USER_DATA_DIR}/{username}.json"
    if not os.path.exists(user_file):
        raise ValueError("Utente non trovato")

    with open(user_file, "r+") as f:
        user_data = json.load(f)
        products = user_data.get("products", [])

        # Filtra il prodotto da eliminare in base all'ASIN
        new_products = [product for product in products if product["asin"] != asin]
        
        # Se il numero di prodotti non cambia, significa che l'ASIN non è stato trovato
        if len(new_products) == len(products):
            raise ValueError("Prodotto non trovato")

        # Aggiorna i prodotti e riscrivi il file JSON
        user_data["products"] = new_products
        f.seek(0)
        json.dump(user_data, f, indent=4)
        f.truncate()

    return {"message": "Prodotto eliminato con successo"}