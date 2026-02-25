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
logger = logging.getLogger(__name__)

def get_asin_from_url(url):
    """Estrae l'ASIN da link Amazon, inclusi quelli con parametri di tracking pubblicitario."""
    decoded_url = unquote(url)
    
    # Prova a trovare direttamente l'ASIN nella parte principale dell'URL
    # Supporta sia /dp/ che /gp/product/
    match = re.search(r"/(?:dp|gp/product)/([A-Z0-9]{10})", decoded_url)
    if match:
        logger.info(f"ASIN estratto direttamente: {match.group(1)}")
        return match.group(1)

    # Se non trovato, cerca all'interno dei parametri della query (per link sponsorizzati)
    parsed_url = urlparse(decoded_url)
    query_params = parse_qs(parsed_url.query)
    
    if 'url' in query_params:
        nested_url = query_params['url'][0]
        match_nested = re.search(r"/dp/([A-Z0-9]{10})", nested_url)
        if match_nested:
            logger.info(f"ASIN estratto dai parametri GET: {match_nested.group(1)}")
            return match_nested.group(1)

    logger.warning("ASIN non trovato nell'URL fornito")
    return None

def clean_price(price):
    """Rimuove simboli di valuta e spazi dal prezzo, restituendo un valore numerico."""
    if not price:
        return None
    price = re.sub(r"[^\d,\.]", "", price)
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

def get_page_content(url, max_retries=5, initial_delay=2):
    """Esegue la richiesta HTTP e restituisce l'oggetto BeautifulSoup."""
    ua = UserAgent()
    session = requests.Session()

    for attempt in range(max_retries):
        try:
            current_ua = ua.random
            headers = {
                "User-Agent": current_ua,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0",
                "DNT": "1",
            }

            logger.info(f"Tentativo {attempt + 1}/{max_retries}...")
            response = session.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                logger.info(f"Successo! Status code: {response.status_code}")
                return BeautifulSoup(response.content, "html.parser")
            elif response.status_code == 503:
                logger.warning("Rilevato 503 Service Unavailable (possibile blocco temporaneo).")
            else:
                logger.warning(f"Status code non valido: {response.status_code}")

            if attempt < max_retries - 1:
                sleep_time = initial_delay * (2 ** attempt) + random.uniform(1, 3)
                logger.info(f"Attesa di {sleep_time:.2f} secondi...")
                time.sleep(sleep_time)
            else:
                raise Exception(f"Impossibile accedere al link Amazon dopo {max_retries} tentativi. Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Errore di rete: {e}")
            if attempt == max_retries - 1:
                raise Exception(f"Errore di rete critico: {e}")
            sleep_time = initial_delay * (2 ** attempt) + random.uniform(1, 3)
            logger.info(f"Attesa di {sleep_time:.2f} secondi...")
            time.sleep(sleep_time)
            
    return None

def parse_title(main_container):
    """Estrae il titolo del prodotto."""
    title_tag = main_container.find(id="productTitle")
    return title_tag.get_text(strip=True) if title_tag else "Titolo non disponibile"

def parse_price_and_condition(main_container):
    """Estrae prezzo e condizione (Nuovo, Usato, ecc.)."""
    condition = "Nuovo"
    price = None

    # Check usato
    used_section = main_container.find("div", {"id": "usedBuySection"})
    if used_section:
        used_price_tag = used_section.find("span", {"class": "a-color-price"})
        if used_price_tag:
            price = clean_price(used_price_tag.get_text(strip=True))
            if price:
                logger.info(f"Prezzo usato trovato: {price}")
                condition = "Usato"

    # Check out of stock
    out_of_stock_section = main_container.find("div", {"id": "outOfStock"})
    if out_of_stock_section:
        logger.info("Prodotto non disponibile (out of stock)")
        condition = "Non disponibile"
        price = None

    # Check nuovo (se non trovato prezzo o condizione è nuovo)
    if price is None and condition == "Nuovo":
        new_price_section = main_container.find("div", {"id": "corePrice_feature_div"})
        if new_price_section:
            price_tag = new_price_section.find("span", {"class": "a-offscreen"})
            if price_tag:
                price = clean_price(price_tag.get_text(strip=True))
                logger.info(f"Prezzo nuovo trovato: {price}")

    return price, condition

def parse_image(main_container):
    """Estrae URL immagine principale."""
    image_tag = main_container.find("img", {"id": "landingImage"})
    return image_tag['src'] if image_tag else None

def parse_rating(main_container):
    """Estrae rating medio."""
    rating_tag = main_container.find("span", {"class": "a-icon-alt"})
    if rating_tag:
        rating_text = rating_tag.get_text(strip=True)
        try:
            return float(rating_text.split(" ")[0].replace(",", "."))
        except (ValueError, AttributeError) as e:
            logger.error(f"Impossibile estrarre il rating: {rating_text}, errore: {e}")
    return None

def parse_details(soup):
    """Estrae dettagli prodotto (tabella)."""
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
    return details

def parse_coupon(soup):
    """Estrae informazioni coupon."""
    coupon = False
    coupon_value = None

    coupon_section = soup.find("i", class_="newCouponBadge")
    if coupon_section:
        logger.info("Coupon trovato")
        coupon_text_container = coupon_section.find_parent("span")
        if coupon_text_container:
            sibling_text = coupon_text_container.get_text(strip=True)
            match = re.search(r"(\d+[.,]?\d*)\s*€", sibling_text)
            if match:
                coupon = True
                coupon_value = match.group(1).replace(",", ".")
                logger.info(f"Valore coupon: {coupon_value}")
            else:
                coupon = True
                logger.info("Coupon presente ma valore non trovato")
                
    return coupon, float(coupon_value) if coupon_value else None

def fetch_product_data(url, max_retries=5, initial_delay=2):
    """Orchestratore dello scraping."""
    logger.info(f"Inizio scraping per URL: {url}")

    asin = get_asin_from_url(url)
    if not asin:
        logger.error("ASIN non trovato nell'URL")
        raise ValueError("ASIN non trovato nell'URL")
    
    logger.info(f"ASIN trovato: {asin}")

    soup = get_page_content(url, max_retries, initial_delay)
    if not soup:
         raise Exception("Impossibile recuperare il contenuto della pagina")

    main_container = soup.find("div", {"id": "dp"})
    if not main_container:
        logger.warning("Contenitore principale del prodotto non trovato (id='dp')")
        raise ValueError("Contenitore principale del prodotto non trovato")

    title = parse_title(main_container)
    price, condition = parse_price_and_condition(main_container)
    image_url = parse_image(main_container)
    rating = parse_rating(main_container)
    details = parse_details(soup)
    coupon, coupon_value = parse_coupon(soup)

    extraction_date = datetime.now().isoformat()
    insertion_date = extraction_date
    
    logger.info("Scraping completato con successo")

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
        "coupon_value": coupon_value
    }
