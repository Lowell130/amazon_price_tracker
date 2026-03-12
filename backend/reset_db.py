import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Carica le variabili d'ambiente dal file .env nella cartella backend
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("Errore: MONGO_URI non trovato. Assicurati che il file .env esista nella cartella backend.")
    exit(1)

def reset_database():
    print(f"Connessione a MongoDB all'URI: {MONGO_URI}")
    client = MongoClient(MONGO_URI)
    db = client["price_tracker"]

    # Cancella i documenti dalla collezione users
    try:
        users_result = db["users"].delete_many({})
        print(f"Cancellati {users_result.deleted_count} documenti dalla collezione 'users'.")
    except Exception as e:
        print(f"Errore durante la cancellazione da 'users': {e}")
        
    # Cancella la collezione products se esiste (per future esecuzioni)
    try:
        products_result = db["products"].delete_many({})
        print(f"Cancellati {products_result.deleted_count} documenti dalla collezione 'products'.")
    except Exception as e:
         print(f"Errore durante la cancellazione da 'products': {e}")

    print("Il database è stato svuotato con successo. Puoi ora procedere e registrare un nuovo utente.")

if __name__ == "__main__":
    reset_database()
