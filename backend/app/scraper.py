from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time
import random
import logging
from urllib.parse import unquote, urlparse, parse_qs
from fake_useragent import UserAgent

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
def fetch_product_data(url, max_retries=5, initial_delay=2):
    """Esegue scraping del titolo, prezzo, immagine e rating del prodotto da un link Amazon."""
    logging.info(f"Inizio scraping per URL: {url}")

    asin = get_asin_from_url(url)
    if not asin:
        logging.error("ASIN non trovato nell'URL")
        raise ValueError("ASIN non trovato nell'URL")
    
    logging.info(f"ASIN trovato: {asin}")

    ua = UserAgent()
    session = requests.Session()

    for attempt in range(max_retries):
        try:
            # Genera un User-Agent casuale per ogni tentativo
            current_ua = ua.random
            
            headers = {
                "User-Agent": current_ua,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0",
            }

            logging.info(f"Tentativo {attempt + 1}/{max_retries}...")
            # logging.info(f"User-Agent: {current_ua}") 

            response = session.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                logging.info(f"Successo! Status code: {response.status_code}")
                break
            elif response.status_code == 503:
                logging.warning("Rilevato 503 Service Unavailable (possibile blocco temporaneo).")
            else:
                logging.warning(f"Status code non valido: {response.status_code}")

            if attempt < max_retries - 1:
                # Exponential backoff con jitter: 2s, 4s, 8s, 16s... + random
                sleep_time = initial_delay * (2 ** attempt) + random.uniform(1, 3)
                logging.info(f"Attesa di {sleep_time:.2f} secondi prima del prossimo tentativo...")
                time.sleep(sleep_time)
            else:
                raise Exception(f"Impossibile accedere al link Amazon dopo {max_retries} tentativi. Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Errore di rete: {e}")
            if attempt == max_retries - 1:
                raise Exception(f"Errore di rete critico: {e}")
            
            sleep_time = initial_delay * (2 ** attempt) + random.uniform(1, 3)
            logging.info(f"Attesa di {sleep_time:.2f} secondi dopo errore di rete...")
            time.sleep(sleep_time)

    soup = BeautifulSoup(response.content, "html.parser")
    main_container = soup.find("div", {"id": "dp"})

    if not main_container:
        logging.warning("Contenitore principale del prodotto non trovato (id='dp')")
        raise ValueError("Contenitore principale del prodotto non trovato")

    logging.info("Contenitore principale trovato")

    title_tag = main_container.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else "Titolo non disponibile"
    logging.info(f"Titolo prodotto: {title}")

    condition = "Nuovo"
    price = None

    used_section = main_container.find("div", {"id": "usedBuySection"})
    if used_section:
        logging.info("Sezione prodotto usato trovata")
        used_price_tag = used_section.find("span", {"class": "a-color-price"})
        if used_price_tag:
            price = clean_price(used_price_tag.get_text(strip=True))
            logging.info(f"Prezzo usato trovato: {price}")
            condition = "Usato"

    out_of_stock_section = main_container.find("div", {"id": "outOfStock"})
    if out_of_stock_section:
        logging.info("Prodotto non disponibile (out of stock)")
        condition = "Non disponibile"
        price = None

    if price is None and condition == "Nuovo":
        logging.info("Ricerca prezzo nuovo...")
        new_price_section = main_container.find("div", {"id": "corePrice_feature_div"})
        if new_price_section:
            price_tag = new_price_section.find("span", {"class": "a-offscreen"})
            if price_tag:
                price = clean_price(price_tag.get_text(strip=True))
                logging.info(f"Prezzo nuovo trovato: {price}")

    image_tag = main_container.find("img", {"id": "landingImage"})
    image_url = image_tag['src'] if image_tag else None
    logging.info(f"Immagine trovata: {image_url}")

    rating = None
    rating_tag = main_container.find("span", {"class": "a-icon-alt"})
    if rating_tag:
        rating_text = rating_tag.get_text(strip=True)
        try:
            rating = float(rating_text.split(" ")[0].replace(",", "."))
            logging.info(f"Rating estratto: {rating}")
        except (ValueError, AttributeError) as e:
            logging.error(f"Impossibile estrarre il rating: {rating_text}, errore: {e}")

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
                continue

    extraction_date = datetime.now().isoformat()
    insertion_date = extraction_date

    coupon = False
    coupon_value = None

    coupon_section = soup.find("i", class_="newCouponBadge")
    if coupon_section:
        logging.info("Coupon trovato")
        coupon_text_container = coupon_section.find_parent("span")
        if coupon_text_container:
            sibling_text = coupon_text_container.get_text(strip=True)
            match = re.search(r"(\d+[.,]?\d*)\s*€", sibling_text)
            if match:
                coupon = True
                coupon_value = match.group(1).replace(",", ".")
                logging.info(f"Valore coupon: {coupon_value}")
            else:
                coupon = True
                logging.info("Coupon presente ma valore non trovato")

    logging.info("Scraping completato con successo")

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
        "insertion_date": insertion_date,
        "price_history": [{"date": extraction_date, "price": price}] if price else [],
        "coupon": coupon,
        "coupon_value": float(coupon_value) if coupon_value else None
    }
