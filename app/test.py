from pymongo import MongoClient
from datetime import datetime
import random
from app.scraper import fetch_product_data
from main import update_prices  # Importa la funzione aggiornata

# Configura il client MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["your_database_name"]  # Sostituisci con il nome del tuo database
users_collection = db["users"]

# Funzione per aggiungere un utente di test con prodotti
def setup_test_data():
    username = "test_user"
    
    # Rimuovi l'utente di test esistente
    users_collection.delete_one({"username": username})
    
    # Crea un utente con prodotti di test
    products = [
        {
            "asin": f"TEST_ASIN_{i}",
            "title": f"Test Product {i}",
            "price": random.uniform(10, 1000),  # Prezzo iniziale casuale
            "price_history": [
                {"date": datetime.now().isoformat(), "price": random.uniform(10, 1000)} for _ in range(5)
            ],
            "product_url": f"https://www.amazon.it/dp/TEST_ASIN_{i}",
            "max_price": None,  # Saranno calcolati dalla funzione
            "min_price": None,
            "average_price": None
        }
        for i in range(3)  # Numero di prodotti di test
    ]

    test_user = {
        "username": username,
        "products": products
    }

    users_collection.insert_one(test_user)
    print("Test data setup complete.")

# Funzione per verificare i risultati dopo l'aggiornamento
def validate_results():
    test_user = users_collection.find_one({"username": "test_user"})
    if not test_user:
        print("Test user not found!")
        return

    for product in test_user["products"]:
        price_history = [entry["price"] for entry in product["price_history"]]
        expected_max = max(price_history)
        expected_min = min(price_history)
        expected_avg = round(sum(price_history) / len(price_history), 2)

        assert product["max_price"] == expected_max, f"Max price mismatch: {product['max_price']} != {expected_max}"
        assert product["min_price"] == expected_min, f"Min price mismatch: {product['min_price']} != {expected_min}"
        assert product["average_price"] == expected_avg, f"Average price mismatch: {product['average_price']} != {expected_avg}"

        print(f"Product {product['asin']} passed validation.")

# Script principale
if __name__ == "__main__":
    setup_test_data()
    
    # Simula un aggiornamento dei prezzi
    update_prices(user_filter="test_user")

    # Valida i risultati nel database
    validate_results()
