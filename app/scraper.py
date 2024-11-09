# app/scraper.py

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

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

def fetch_product_data(url, max_retries=3, delay=2):
    """Esegue scraping del titolo, prezzo e immagine del prodotto dal link Amazon."""
    asin = get_asin_from_url(url)
    if not asin:
        raise ValueError("ASIN non trovato nell'URL")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break
        elif attempt < max_retries - 1:
            time.sleep(delay)  # Attende prima di riprovare
        else:
            raise Exception("Impossibile accedere al link Amazon dopo vari tentativi")

    soup = BeautifulSoup(response.content, "html.parser")

    # Estrazione e pulizia del titolo
    title = soup.find(id="productTitle")
    title = clean_text(title.get_text(strip=True)) if title else "Titolo non disponibile"

    # Estrazione e pulizia del prezzo
    price_tag = soup.find("span", {"class": "a-offscreen"})
    price = clean_price(price_tag.get_text(strip=True)) if price_tag else None

    # Estrazione dell'URL dell'immagine
    image_tag = soup.find("img", {"id": "landingImage"})
    image_url = image_tag['src'] if image_tag else None

    if price is None:
        return None

    # Creiamo il dizionario con i dati del prodotto
    product_data = {
        "asin": asin,
        "title": title,
        "price": price,
        "image_url": image_url,  # Aggiunge l'URL dell'immagine
        "extraction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price_history": [{"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "price": price}]
    }
    return product_data
