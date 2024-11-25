import json
import os
from app.db import users_collection  # Assumendo che `app` contenga la configurazione di MongoDB

# Definisci il percorso assoluto alla cartella `data`
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "users")  # Aggiorna per puntare a `data/users`

# Funzione per importare i dati JSON in MongoDB
def import_data_to_mongodb():
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(f"La directory {DATA_DIR} non esiste")

    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith(".json"):
            file_path = os.path.join(DATA_DIR, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                user_data = json.load(file)
                username = user_data.get("username")
                if not username:
                    print(f"Errore: il file {file_name} non contiene un campo `username`")
                    continue
                # Salva i dati su MongoDB
                users_collection.update_one(
                    {"username": username},
                    {"$set": user_data},
                    upsert=True
                )
                print(f"Dati per {username} importati con successo!")

if __name__ == "__main__":
    import_data_to_mongodb()
