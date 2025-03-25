from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Carica le variabili di ambiente
load_dotenv()

# Connetti al DB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["price_tracker"]
users_collection = db["users"]

# Funzione per aggiornare tutti i prodotti nei documenti utente
def update_all_products_add_coupon_field():
    result = users_collection.update_many(
        {},
        {
            "$set": {
                "products.$[].coupon": False,
                "products.$[].coupon_value": None
            }
        }
    )
    print(f"Documenti modificati: {result.modified_count}")

if __name__ == "__main__":
    update_all_products_add_coupon_field()
