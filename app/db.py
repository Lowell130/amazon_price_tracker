from pymongo import MongoClient

# Hardcoded URI per testare la connessione
MONGO_URI = "mongodb+srv://testUser:bD91w6E9qvhx6z8a@cluster0.fve8hpt.mongodb.net/"

# Connettiti a MongoDB
client = MongoClient(MONGO_URI)
db = client["price_tracker"]
users_collection = db["users"]


print("Connesso con successo al database remoto!")
