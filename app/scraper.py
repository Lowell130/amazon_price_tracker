from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time
import random
import logging
from urllib.parse import unquote, urlparse, parse_qs

# Configura il logging
logging.basicConfig(level=logging.INFO)

def get_asin_from_url(url):
    """Estrae l'ASIN da link Amazon, inclusi quelli con parametri di tracking pubblicitario."""
    # Decodifica l'URL per gestire link con parametri GET complessi
    decoded_url = unquote(url)
    
    # Prova a trovare direttamente l'ASIN nella parte principale dell'URL
    match = re.search(r"/dp/([A-Z0-9]{10})", decoded_url)
    if match:
        logging.info(f"ASIN estratto direttamente: {match.group(1)}")
        return match.group(1)

    # Se non trovato, cerca all'interno dei parametri della query (per link sponsorizzati)
    parsed_url = urlparse(decoded_url)
    query_params = parse_qs(parsed_url.query)
    
    if 'url' in query_params:
        nested_url = query_params['url'][0]  # Prende il primo valore
        match_nested = re.search(r"/dp/([A-Z0-9]{10})", nested_url)
        if match_nested:
            logging.info(f"ASIN estratto dai parametri GET: {match_nested.group(1)}")
            return match_nested.group(1)

    logging.warning("ASIN non trovato nell'URL fornito")
    return None

def clean_price(price):
    """Rimuove simboli di valuta e spazi dal prezzo, restituendo un valore numerico."""
    price = re.sub(r"[^\d,\.]", "", price)  # Mantiene solo numeri, virgole e punti
    if "," in price and "." in price:
        if price.index(",") > price.index("."):
            price = price.replace(".", "").replace(",", ".")
        else:
            price = price.replace(",", "")
    elif "," in price:
        price = price.replace(",", ".")
    
    try:
        return float(price)
    except ValueError:
        return None

def fetch_product_data(url, max_retries=3, delay=2):
    """Esegue scraping del titolo, prezzo, immagine e rating del prodotto da un link Amazon."""
    asin = get_asin_from_url(url)
    if not asin:
        raise ValueError("ASIN non trovato nell'URL")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9"
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

    # Identificazione e gestione delle diverse condizioni del prodotto
    condition = "Nuovo"
    price = None

    # 1. Controllo se il prodotto è usato
    used_section = main_container.find("div", {"id": "usedBuySection"})
    if used_section:
        used_price_tag = used_section.find("span", {"class": "a-color-price"})
        if used_price_tag:
            price = clean_price(used_price_tag.get_text(strip=True))
            condition = "Usato"

    # 2. Controllo se il prodotto è non disponibile
    out_of_stock_section = main_container.find("div", {"id": "outOfStock"})
    if out_of_stock_section:
        condition = "Non disponibile"
        price = None

    # 3. Altrimenti, cerca il prezzo per un prodotto nuovo
    if price is None and condition == "Nuovo":
        new_price_section = main_container.find("div", {"id": "corePrice_feature_div"})
        if new_price_section:
            price_tag = new_price_section.find("span", {"class": "a-offscreen"})
            if price_tag:
                price = clean_price(price_tag.get_text(strip=True))

    # Estrazione dell'URL dell'immagine
    image_tag = main_container.find("img", {"id": "landingImage"})
    image_url = image_tag['src'] if image_tag else None

    # Estrazione del rating
    rating = None
    rating_tag = main_container.find("span", {"class": "a-icon-alt"})
    if rating_tag:
        rating_text = rating_tag.get_text(strip=True)
        try:
            rating = float(rating_text.split(" ")[0].replace(",", "."))
            logging.info(f"Rating estratto: {rating}")
        except (ValueError, AttributeError) as e:
            logging.error(f"Impossibile estrarre il rating: {rating_text}, errore: {e}")

    # Estrazione dettagli prodotto
    details = []
    details_section = soup.find("table", class_="a-normal a-spacing-micro")
    if details_section:
        rows = details_section.find_all("tr")
        for row in rows:
            try:
                key = row.find("td", class_="a-span3").get_text(strip=True)
                value = row.find("td", class_="a-span9").get_text(strip=True)
                details.append({key: value})
            except AttributeError:
                continue  # Ignora righe che non seguono la struttura prevista

    # Data di estrazione
    extraction_date = datetime.now().isoformat()
    insertion_date = extraction_date  # Usa lo stesso timestamp della data di estrazione


    # Ritorna i dati del prodotto
    return {
        "asin": asin,
        "title": title,
        "price": price,
        "condition": condition,
        "image_url": image_url,
        "rating": rating,
        "availability": "Disponibile" if condition != "Non disponibile" else "Non disponibile",
        "details": details,
        "extraction_date": extraction_date,
        "insertion_date": insertion_date,  # ✅ Aggiunto nuovamente
        "price_history": [{"date": extraction_date, "price": price}] if price else [],
    }
