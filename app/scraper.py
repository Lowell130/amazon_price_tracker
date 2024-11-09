# app/scraper.py
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def get_asin_from_url(url):
    """Estrae l'ASIN dal link Amazon."""
    match = re.search(r"/([A-Z0-9]{10})(?:[/?]|$)", url)
    return match.group(1) if match else None

def clean_price(price):
    """Rimuove simboli di valuta e spazi dal prezzo, restituendo un valore numerico come stringa."""
    return re.sub(r"[^\d,\.]", "", price).replace(",", ".")

def clean_text(text):
    """Rimuove caratteri unicode problematici e pulisce il testo."""
    return text.replace("\u20ac", "EUR").replace("'", "").replace("\"", "").strip()

def fetch_product_data(url):
    """Esegue scraping del titolo e prezzo del prodotto dal link Amazon."""
    asin = get_asin_from_url(url)
    if not asin:
        raise ValueError("ASIN non trovato nell'URL")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Impossibile accedere al link Amazon")

    soup = BeautifulSoup(response.content, "html.parser")

    # Estrazione e pulizia del titolo
    title = soup.find(id="productTitle")
    title = clean_text(title.get_text(strip=True)) if title else "Titolo non disponibile"

    # Estrazione e pulizia del prezzo
    price_tag = soup.find("span", {"class": "a-offscreen"})
    price = clean_price(price_tag.get_text(strip=True)) if price_tag else "Prezzo non disponibile"

    # Creiamo il dizionario con i dati del prodotto
    product_data = {
        "asin": asin,
        "title": title,
        "price": price,
        "extraction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price_history": [{"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "price": price}]
    }
    return product_data
