from pymongo import MongoClient

# Connettiti a MongoDB
client = MongoClient("mongodb+srv://testUser:bD91w6E9qvhx6z8a@cluster0.fve8hpt.mongodb.net/")
db = client["price_tracker"]
users_collection = db["users"]

# Aggiorna tutti i prodotti esistenti
for user in users_collection.find():
    updated_products = []
    for product in user.get("products", []):
        if "is_favorite" not in product:
            product["is_favorite"] = False
        updated_products.append(product)

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"products": updated_products}}
    )

print("Aggiornamento completato!")
