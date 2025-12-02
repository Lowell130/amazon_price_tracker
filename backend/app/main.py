from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, products, admin, public
from app.db import users_collection
from app.config import BASE_URL
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "https://amazon-price-tracker-delta.vercel.app",
    "amazon-price-tracker-git-main-lowell130s-projects.vercel.app",
    "amazon-price-tracker-ndlrmkzir-lowell130s-projects.vercel.app",
    "https://pricehub.it",
    "https://www.pricehub.it",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(admin.router)
app.include_router(public.router)

@app.get("/sitemap.xml", response_class=Response)
async def generate_sitemap():
    """
    Genera una sitemap dinamica in XML con i prodotti disponibili nel database.
    """
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Homepage
    url = SubElement(urlset, "url")
    SubElement(url, "loc").text = f"{BASE_URL}/"
    SubElement(url, "lastmod").text = datetime.today().strftime("%Y-%m-%d")
    SubElement(url, "priority").text = "1.0"

    # Pagina prodotti
    url = SubElement(urlset, "url")
    SubElement(url, "loc").text = f"{BASE_URL}/products"
    SubElement(url, "lastmod").text = datetime.today().strftime("%Y-%m-%d")
    SubElement(url, "priority").text = "0.8"

    # Recupera tutti i prodotti dal database
    products_cursor = users_collection.find({}, {"products": 1})
    all_products = []

    for user in products_cursor:
        if "products" in user:
            all_products.extend(user["products"])

    # Genera un URL per ogni prodotto
    for product in all_products:
        product_url = f"{BASE_URL}/products/{product['asin']}"
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = product_url
        SubElement(url, "lastmod").text = datetime.today().strftime("%Y-%m-%d")
        SubElement(url, "priority").text = "0.7"

    # Converti in stringa XML
    xml_data = tostring(urlset, encoding="utf-8", method="xml")

    return Response(content=xml_data, media_type="application/xml")

@app.get("/")
async def root():
    return {"message": "Amazon Price Tracker API"}
