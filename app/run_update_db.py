from pymongo import MongoClient

# Configura la connessione al database
MONGO_URI = "mongodb+srv://testUser:bD91w6E9qvhx6z8a@cluster0.fve8hpt.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["price_tracker"]
users_collection = db["users"]

print("Connesso con successo al database remoto!")

# Funzione per aggiungere il campo `condition` ai prodotti
def add_condition_field():
    # Trova tutti gli utenti nella collezione `users`
    users = users_collection.find()

    for user in users:
        user_id = user["_id"]
        products = user.get("products", [])

        updated_products = []
        for product in products:
            # Aggiungi il campo `condition` se non esiste
            if "condition" not in product:
                product["condition"] = "Unavailable"  # Valore predefinito
            updated_products.append(product)

        # Aggiorna i prodotti per l'utente nel database
        users_collection.update_one(
            {"_id": user_id},
            {"$set": {"products": updated_products}}
        )
        print(f"Campo `condition` aggiunto per l'utente con ID: {user_id}")

# Esegui lo script
add_condition_field()

print("Aggiornamento completato!")
