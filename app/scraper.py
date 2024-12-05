#scraper.py


from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time
import random

def get_asin_from_url(url):
    """Estrae l'ASIN dal link Amazon."""
    match = re.search(r"/([A-Z0-9]{10})(?:[/?]|$)", url)
    return match.group(1) if match else None

def clean_price(price):
    """
    Rimuove simboli di valuta e spazi dal prezzo, restituendo un valore numerico come stringa normalizzata.
    Gestisce correttamente i prezzi sopra le migliaia.
    """
    price = re.sub(r"[^\d,\.]", "", price)  # Rimuove simboli non numerici eccetto la virgola e il punto
    if "," in price and "." in price:
        if price.index(",") > price.index("."):
            price = price.replace(".", "").replace(",", ".")
        else:
            price = price.replace(",", "")
    elif "," in price:
        price = price.replace(",", ".")
    return float(price)

def clean_text(text):
    """Rimuove caratteri unicode problematici e pulisce il testo."""
    return text.replace("\u20ac", "EUR").replace("'", "").replace("\"", "").strip()

def fetch_product_data(url, max_retries=3, delay=2):
    """Esegue scraping del titolo, prezzo e immagine del prodotto dal link Amazon."""
    asin = get_asin_from_url(url)
    if not asin:
        raise ValueError("ASIN non trovato nell'URL")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9"  # Specifica la lingua desiderata
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                break
            elif attempt < max_retries - 1:
                time.sleep(delay + random.uniform(0, 1))
            else:
                raise Exception("Impossibile accedere al link Amazon dopo vari tentativi")
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise Exception(f"Errore di rete durante l'accesso al link Amazon: {e}")
            time.sleep(delay + random.uniform(0, 1))

    soup = BeautifulSoup(response.content, "html.parser")
    main_container = soup.find("div", {"id": "dp"})
    if not main_container:
        raise ValueError("Contenitore principale del prodotto non trovato")

    # Estrazione e pulizia del titolo
    title_tag = main_container.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else "Titolo non disponibile"

    # Controllo disponibilità
    availability_tag = main_container.find("div", {"id": "availability"})
    availability_text = availability_tag.get_text(strip=True) if availability_tag else ""
    if "non disponibile" in availability_text.lower() or "currently unavailable" in availability_text.lower():
        return {
            "asin": asin,
            "title": title,
            "price": None,
            "image_url": None,
            "availability": "Non disponibile",
            "extraction_date": datetime.now().isoformat(),
            "price_history": []
        }

    # Estrazione del prezzo
    price_tag = (
        main_container.find("span", {"class": "a-offscreen"}) or
        main_container.find("span", {"id": "priceblock_ourprice"}) or
        main_container.find("span", {"id": "priceblock_dealprice"})
    )
    price = clean_price(price_tag.get_text(strip=True)) if price_tag else None

    # Estrazione dell'URL dell'immagine
    image_tag = main_container.find("img", {"id": "landingImage"})
    image_url = image_tag['src'] if image_tag else None

    return {
        "asin": asin,
        "title": title,
        "price": price,
        "image_url": image_url,
        "availability": "Disponibile",
        "extraction_date": datetime.now().isoformat(),
        "price_history": [{"date": datetime.now().isoformat(), "price": price}]
    }
