#db.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Leggi la URI dal file .env
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI non è configurato. Aggiungi questa variabile al file .env.")

# Connettiti a MongoDB
client = MongoClient(MONGO_URI)
db = client["price_tracker"]
users_collection = db["users"]
public_alerts_collection = db["public_alerts"]


print("Connesso con successo al database remoto!")
