#main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router, get_current_user
from app.scraper import fetch_product_data
from app.db import users_collection
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from bson.objectid import ObjectId
from typing import List
from typing import Optional  # Aggiunto import
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.db import users_collection

router = APIRouter()

# Configura il logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# Carica le variabili dal file .env
load_dotenv()

# Recupera le informazioni dal file .env
affiliate_tag = os.getenv("AFFILIATE_TAG")

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://amazon-price-tracker-delta.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(auth_router, prefix="/api")

class ProductRequest(BaseModel):
    product_url: str
    category: Optional[str] = None  # Campo facoltativo per la categoria


def admin_required(current_user: str = Depends(get_current_user)):
    user = users_collection.find_one({"username": current_user})
    if not user or not user.get("admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required"
        )
    return user


@app.post("/api/admin/generate-price-drops-report", dependencies=[Depends(admin_required)])
async def generate_price_drops_report():
    """
    Genera una collezione separata con tutte le variazioni di prezzo in positivo.
    Accessibile solo agli amministratori.
    """
    try:
        price_drops_collection = users_collection.database["price_drops"]

        # Rimuove i dati precedenti nella collezione
        price_drops_collection.delete_many({})

        # Analizza gli utenti e i prodotti
        users = users_collection.find({})
        report = {
            "generation_date": datetime.now().isoformat(),
            "drops": []  # Array che contiene tutte le variazioni
        }

        for user in users:
            for product in user.get("products", []):
                price_history = product.get("price_history", [])
                if len(price_history) < 2:
                    continue  # Non ci sono abbastanza dati per calcolare una variazione

                # Ordina per data
                price_history = sorted(price_history, key=lambda x: x["date"])
                old_price = price_history[-2]["price"]
                new_price = price_history[-1]["price"]

                if new_price < old_price:  # Verifica calo di prezzo
                    report["drops"].append({
                        "asin": product["asin"],
                        "title": product["title"],
                        "old_price": old_price,
                        "new_price": new_price,
                        "price_drop": round(old_price - new_price, 2),
                        "user": user["username"],
                        "category": product.get("category"),
                        "date": price_history[-1]["date"],
                        "affiliate": product.get("affiliate"),
                        "condition": product.get("condition", "Unknown"),
                        "image_url": product.get("image_url", ""),
                        "rating": product.get("rating", None),
                        "availability": product.get("availability", "Unknown"),
                        "insertion_date": product.get("insertion_date", None),
                    })

        # Inserisce i dati nella nuova collezione come un singolo documento
        price_drops_collection.insert_one(report)

        return {
            "message": "Price drops report generated",
            "total_price_drops": len(report["drops"]),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@app.get("/api/product-details/{asin}")
async def product_details(asin: str, current_user: str = Depends(get_current_user)):
    """
    Ottiene i dettagli completi di un prodotto specifico dato l'ASIN.
    """
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    product = next((p for p in db_user.get("products", []) if p["asin"] == asin), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.post("/api/update-selected-prices/")
async def update_selected_prices(
    asin_list: List[str],  # Riceve una lista di ASIN dal body della richiesta
    current_user: str = Depends(get_current_user)
):
    """Aggiorna manualmente i prezzi solo per i prodotti selezionati dall'utente."""
    if not asin_list:
        raise HTTPException(status_code=400, detail="ASIN list cannot be empty")

    try:
        updated_products = update_prices(user_filter=current_user, asin_filter=asin_list)
        return {"message": "Selected product prices updated", "updated_products": updated_products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating selected products: {str(e)}")


@app.post("/api/add-product/")
async def add_product(request: ProductRequest, current_user: str = Depends(get_current_user)):
    """
    Aggiunge un prodotto per l'utente corrente, includendo i dettagli estratti.
    """
    # Recupera l'utente dal database
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Esegue scraping del prodotto
    product_data = fetch_product_data(request.product_url)
    if not product_data or not product_data.get("price"):
        raise HTTPException(status_code=400, detail="Error fetching product data")

    asin = product_data["asin"]

    # Verifica che l'ASIN non sia già monitorato
    if any(product["asin"] == asin for product in db_user.get("products", [])):
        raise HTTPException(status_code=400, detail="Product already being tracked")

    # Genera il link affiliato
    affiliate_link = f"https://www.amazon.it/gp/product/{asin}/?tag={affiliate_tag}"

    # Aggiunge i dati del prodotto
    product_data.update({
        "product_url": request.product_url,
        "category": request.category,
        "affiliate": affiliate_link,
    })

    # Salva nel database
    users_collection.update_one(
        {"_id": db_user["_id"]},
        {"$push": {"products": product_data}}
    )
    return {"message": "Product added successfully", "affiliate": affiliate_link}


@app.get("/api/product-details/{asin}")
async def product_details(asin: str, current_user: str = Depends(get_current_user)):
    """
    Ottiene i dettagli completi di un prodotto specifico dato l'ASIN.
    """
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    product = next((p for p in db_user.get("products", []) if p["asin"] == asin), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "asin": product["asin"],
        "title": product["title"],
        "current_price": product["price"],
        "max_price": product["max_price"],
        "min_price": product["min_price"],
        "average_price": product["average_price"],
        "price_history": product["price_history"],
        "details": product.get("details", [])  # Aggiungi i dettagli
    }


@app.patch("/api/favorite/{asin}")
async def toggle_favorite(asin: str, current_user: str = Depends(get_current_user)):
    """
    Aggiorna il campo `is_favorite` per un prodotto specifico.
    """
    # Recupera l'utente dal database
    db_user = users_collection.find_one({"username": current_user})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Trova il prodotto nell'elenco
    products = db_user.get("products", [])
    product = next((p for p in products if p["asin"] == asin), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Aggiorna lo stato del preferito
    new_favorite_status = not product.get("is_favorite", False)
    users_collection.update_one(
        {"_id": db_user["_id"], "products.asin": asin},
        {"$set": {"products.$.is_favorite": new_favorite_status}}
    )

    return {"message": "Favorite status updated", "is_favorite": new_favorite_status}


@app.post("/api/update-prices-manual/")
async def update_prices_manual(current_user: str = Depends(get_current_user)):
    """Aggiorna manualmente i prezzi dei prodotti per l'utente corrente."""
    try:
        update_prices(user_filter=current_user)
        return {"message": "Price update triggered manually"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during manual price update")
    

# Funzione per inviare email
def send_email(to_email, product_title, old_price, new_price):
    sender_email = "blackfdayit@gmail.com"  # Inserisci la tua email
    sender_password = "zxbt cnqg ckqe tqbq"  # Inserisci la tua password o un token
    subject = f"📉 Price Drop Alert: {product_title}"
    body = f"""
    Il prodotto "{product_title}" che hai aggiunto ai preferiti ha subito un calo di prezzo!

    Prezzo precedente: {old_price} €
    Nuovo prezzo: {new_price} €

    Affrettati a controllare!
    """

    # Configura SMTP
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Configura il server SMTP
        server.starttls()
        server.login(sender_email, sender_password)

        # Creazione del messaggio
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"Email inviata a {to_email} per il prodotto {product_title}")
    except Exception as e:
        print(f"Errore durante l'invio dell'email: {e}")


def update_prices(user_filter=None, asin_filter=None):
    query = {"username": user_filter} if user_filter else {}
    users = users_collection.find(query)
    updated_products = []

    for user in users:
        email = user.get("email")  # Assumiamo che l'email sia salvata nel profilo utente
        products = user.get("products", [])
        logger.info(f"Updating prices for user: {user['username']} ({len(products)} products)")

        for product in products:
            if asin_filter and product["asin"] not in asin_filter:
                continue

            try:
                logger.info(f"Fetching product data for ASIN: {product['asin']}")
                updated_data = fetch_product_data(product["product_url"])

                if not updated_data or updated_data["price"] is None:
                    product["availability"] = "Non disponibile"
                    product["condition"] = "Non disponibile"
                    logger.info(f"Product {product['asin']} is unavailable.")
                    continue

                old_price = float(product["price"]) if product["price"] else None
                new_price = float(updated_data["price"])

                if product.get("is_favorite", False) and old_price and new_price < old_price:
                    logger.info(f"Price drop detected for {product['title']}. Sending email.")
                    send_email(email, product["title"], old_price, new_price)

                product["price_history"].append({"date": datetime.now().isoformat(), "price": new_price})
                product["price"] = new_price
                product["availability"] = "Disponibile"
                product["condition"] = updated_data["condition"]

                # Calcola max, min, e average price
                price_history = product["price_history"]
                max_price_entry = max(price_history, key=lambda x: float(x["price"]))
                min_price_entry = min(price_history, key=lambda x: float(x["price"]))

                product["max_price"] = float(max_price_entry["price"])
                product["min_price"] = float(min_price_entry["price"])
                product["average_price"] = round(
                    sum(float(entry["price"]) for entry in price_history) / len(price_history), 2
                )

                updated_products.append(product["asin"])
                logger.info(f"Updated product {product['asin']} - New Price: {new_price} €")

            except Exception as e:
                logger.error(f"Error updating product {product['asin']}: {e}")
                continue

        users_collection.update_one({"_id": user["_id"]}, {"$set": {"products": products}})
        logger.info(f"Finished updating products for user: {user['username']}")

    return updated_products


@app.get("/api/public/price-drops")
async def get_price_drops(
    category: Optional[str] = None,
    limit: int = Query(42, ge=1, le=100),  # Limita il numero di risultati per pagina
    skip: int = Query(0, ge=0)  # Salta i primi N risultati
):
    """
    Restituisce i prodotti con diminuzione di prezzo.
    - `category`: filtro opzionale per categoria.
    - `limit`: numero massimo di risultati da restituire (default 10, massimo 100).
    - `skip`: salta i primi N risultati (default 0).
    """
    try:
        price_drops_collection = users_collection.database["price_drops"]
        price_drops_data = price_drops_collection.find_one(sort=[("generation_date", -1)])
        
        if not price_drops_data:
            raise HTTPException(status_code=404, detail="No price drops found.")

        drops = price_drops_data["drops"]
        
        # Filtra per categoria se specificato
        if category:
            drops = [drop for drop in drops if drop.get("category") == category]
        
        # Escludi i prodotti con "condition" uguale a "Non disponibile"
        drops = [drop for drop in drops if drop.get("condition") != "Non disponibile"]

        # Ordina per calo di prezzo (descrescente)
        drops.sort(key=lambda x: x.get("price_drop", 0), reverse=True)

        # Paginazione
        total_drops = len(drops)
        drops = drops[skip : skip + limit]

        return {
            "total_drops": total_drops,
            "displayed_drops": len(drops),
            "data": drops
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving price drops: {str(e)}")




app.include_router(router)



@app.post("/api/update-product/{asin}")
async def update_product_price(asin: str, current_user: str = Depends(get_current_user)):
    """
    Aggiorna manualmente il prezzo di un singolo prodotto.
    """
    try:
        # Chiamata per aggiornare i prezzi solo per un prodotto specifico
        updated_products = update_prices(user_filter=current_user, asin_filter=[asin])

        # Verifica se il prodotto è stato aggiornato
        if not updated_products:
            raise HTTPException(status_code=404, detail="Product not found or not updated")

        # Recupera i dettagli aggiornati del prodotto
        db_user = users_collection.find_one({"username": current_user})
        product = next((p for p in db_user.get("products", []) if p["asin"] == asin), None)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found after update")

        return {
            "message": f"Product {asin} updated successfully",
            "product": {
                "asin": product["asin"],
                "price": product["price"],
                "price_history": product["price_history"],
                "max_price": product["max_price"],
                "min_price": product["min_price"],
                "average_price": product["average_price"],
                "availability": product.get("availability", "Unknown"),
                "condition": product.get("condition", "Unknown"),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")


scheduler = BackgroundScheduler()
scheduler.add_job(update_prices, 'interval', hours=5)
scheduler.start()




@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Amazon Price Tracker API"}
