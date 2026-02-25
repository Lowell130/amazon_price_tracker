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

def get_db():
    """Dependency provider for the database."""
    return db

def get_users_collection():
    """Dependency provider for users collection."""
    return db["users"]

def get_public_alerts_collection():
    """Dependency provider for public alerts collection."""
    return db["public_alerts"]

# Export global variables for backward compatibility if needed, 
# but mostly we should use dependencies.
# Keeping these for now to avoid breaking imports I haven't changed yet, 
# but the goal is to replace their usage.
users_collection = db["users"]
public_alerts_collection = db["public_alerts"]

print("Connesso con successo al database remoto!")
