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

from app.db import get_settings_collection

def get_asin_from_url(url):
    """Estrae l'ASIN da link Amazon, inclusi quelli con parametri di tracking pubblicitario."""
    decoded_url = unquote(url)
    
    # Prova a trovare direttamente l'ASIN nella parte principale dell'URL
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

def get_random_headers():
    """Genera header realistici per simulare un browser reale."""
    ua = UserAgent()
    user_agent = ua.random
    
    # Header di base comuni per browser moderni
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": random.choice(["it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7", "it-IT,it;q=0.9", "en-US,en;q=0.9"]),
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "DNT": "1",
        "Cache-Control": "max-age=0",
        "Referer": random.choice([
            "https://www.google.it/",
            "https://www.bing.com/",
            "https://duckduckgo.com/",
            "https://www.amazon.it/"
        ]),
        "device-memory": random.choice(["4", "8", "16"]),
        "viewport-width": str(random.randint(1200, 1920)),
    }
    
    # Aggiungi meta-dati specifici per simulare meglio Chrome se l'User-Agent è Chrome
    if "Chrome" in user_agent:
        headers["sec-ch-ua"] = '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'
        headers["sec-ch-ua-mobile"] = "?0"
        headers["sec-ch-ua-platform"] = '"Windows"'
        
    return headers

def get_page_content(url, max_retries=7, initial_delay=3, proxies=None):
    """Recupera il contenuto HTML della pagina con retry, headers casuali e supporto proxy."""
    session = requests.Session()
    
    for attempt in range(max_retries):
        try:
            headers = get_random_headers()
            # Imposta l'host correttamente
            parsed_url = urlparse(url)
            headers["Host"] = parsed_url.netloc
            
            logger.info(f"Tentativo {attempt + 1}/{max_retries}...")
            
            # Aggiunge un piccolo timeout variabile per evitare pattern fissi
            response = session.get(url, headers=headers, timeout=25, proxies=proxies)
            
            if response.status_code == 200:
                # Verifica se siamo finiti su una pagina di CAPTCHA
                if "api-services-support@amazon.com" in response.text or "sp-cc-container" in response.text or "captcha" in response.text.lower():
                    if "sp-cc-container" in response.text and "productTitle" in response.text:
                         # Potrebbe essere solo il banner dei cookie su una pagina valida
                         return BeautifulSoup(response.content, "html.parser")
                    logger.warning("Rilevato possibile CAPTCHA o blocco bot.")
                else:
                    logger.info(f"Successo! Status code: {response.status_code}")
                    return BeautifulSoup(response.content, "html.parser")
            
            elif response.status_code == 404:
                logger.warning(f"Errore 404 per {url}. Possibile blocco o URL errato.")
            elif response.status_code == 403:
                logger.warning("Errore 403 Forbidden (accesso negato/blocco IP).")
            elif response.status_code == 503:
                logger.warning("Errore 503 Service Unavailable (sovraccarico o blocco).")
            else:
                logger.warning(f"Status code inatteso: {response.status_code}")

            if attempt < max_retries - 1:
                # Backoff esponenziale più aggressivo con jitter
                sleep_time = min(120, initial_delay * (2 ** attempt) + random.uniform(5, 10))
                logger.info(f"Attesa di {sleep_time:.2f} secondi prima del prossimo tentativo...")
                time.sleep(sleep_time)
            else:
                logger.error(f"Fallito dopo {max_retries} tentativi. Ultimo status: {response.status_code}")
                # Fallback: restituisci il soup se abbiamo un 200 (anche con captcha) per debug
                if response.status_code == 200:
                    return BeautifulSoup(response.content, "html.parser")

        except requests.exceptions.RequestException as e:
            logger.error(f"Errore di rete al tentativo {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                sleep_time = initial_delay * (2 ** attempt) + random.uniform(5, 10)
                time.sleep(sleep_time)
            else:
                raise Exception(f"Errore di rete critico dopo {max_retries} tentativi: {e}")
            
    return None

def parse_title(soup):
    """Estrae il titolo del prodotto con selettori multipli."""
    selectors = [
        {"id": "productTitle"},
        {"id": "title"},
        {"class": "a-size-large product-title-word-break"},
        {"id": "item_name"}
    ]
    
    for selector in selectors:
        tag = soup.find(**selector)
        if tag:
            title = tag.get_text(strip=True)
            if title:
                return title
                
    return "Titolo non disponibile"

def parse_price_and_condition(soup):
    """Estrae prezzo e condizione con logica robusta e fallback."""
    condition = "Nuovo"
    price = None

    # 1. Check Out of Stock
    out_of_stock_selectors = [
        {"id": "outOfStock"},
        {"id": "availability", "string": re.compile(r"Non disponibile|Attualmente non disponibile", re.I)},
    ]
    for sel in out_of_stock_selectors:
        if soup.find(**sel):
            logger.info("Prodotto non disponibile (out of stock)")
            return None, "Non disponibile"

    # 2. Check Usato
    used_selectors = [
        {"id": "usedBuySection"},
        {"id": "usedAndNew_feature_div"},
        {"class": "olp-used"}
    ]
    for sel in used_selectors:
        used_section = soup.find(**sel)
        if used_section:
            used_price_tag = used_section.find(class_=re.compile(r"a-color-price|a-offscreen"))
            if used_price_tag:
                price = clean_price(used_price_tag.get_text(strip=True))
                if price:
                    logger.info(f"Prezzo usato trovato: {price}")
                    return price, "Usato"

    # 3. Check Nuovo (Selettori multipli)
    new_price_selectors = [
        {"id": "corePrice_feature_div"},
        {"id": "corePriceDisplay_desktop_feature_div"},
        {"id": "corePrice_desktop"},
        {"class": "a-price a-text-price a-size-medium apexPriceToPay"},
        {"id": "priceDirectBuy"},
        {"id": "priceblock_ourprice"},
        {"id": "priceblock_dealprice"}
    ]
    
    for sel in new_price_selectors:
        section = soup.find(**sel)
        if section:
            # Cerca il prezzo "offscreen" o il simbolo dell'euro
            price_tag = section.find(class_="a-offscreen") or section.find(string=re.compile(r"€"))
            if price_tag:
                text = price_tag.get_text(strip=True) if hasattr(price_tag, 'get_text') else str(price_tag)
                price = clean_price(text)
                if price:
                    logger.info(f"Prezzo nuovo trovato ({sel}): {price}")
                    return price, "Nuovo"

    # Fallback estremo: cerca qualsiasi cosa che sembri un prezzo nel contenitore principale
    main_dp = soup.find(id="dp")
    if main_dp:
        all_prices = main_dp.find_all(class_="a-offscreen")
        for p in all_prices:
            val = clean_price(p.get_text(strip=True))
            if val and val > 0:
                logger.info(f"Prezzo trovato tramite fallback generico: {val}")
                return val, "Nuovo"

    return None, condition

def parse_data_from_json(soup):
    """Estrae i dati fondamentali dai blocchi JSON della pagina."""
    price = None
    availability = "Disponibile"
    condition = "Nuovo"
    
    # Lista di pattern JSON per il prezzo in ordine di affidabilità
    price_patterns = [
        r'"priceAmount":\s*(\d+\.?\d*)',
        r'"priceToPay":\s*(\d+\.?\d*)',
        r'"buyingPrice":\s*(\d+\.?\d*)',
        r'"value":\s*(\d+\.?\d*),\s*"currency":\s*"EUR"',
        r'"displayPrice":\s*"(.*?)"'
    ]
    
    scripts = soup.find_all("script")
    for s in scripts:
        if not s.string:
            continue
            
        script_content = s.string
        
        # 1. Cerca il blocco twister-js-init-dpx-data
        if "twister-js-init-dpx-data" in script_content:
            logger.info("Analisi blocco twister-js-init-dpx-data...")
            for pattern in price_patterns:
                match = re.search(pattern, script_content)
                if match:
                    val = match.group(1)
                    # Se è un displayPrice (stringa con €), puliscilo
                    if "€" in val or "," in val:
                        price = clean_price(val)
                    else:
                        price = float(val)
                    
                    if price:
                        logger.info(f"Prezzo trovato in twister JSON ({pattern}): {price}")
                        break
            
            if not price:
                # Prova estrazione più profonda se twister è presente ma i pattern falliscono
                logger.info("Deep search nel blocco twister...")
                # Cerchiamo blocchi del tipo "price": {"amount": 123.45}
                deep_price = re.search(r'"price":\s*\{\s*"amount":\s*(\d+\.?\d*)', script_content)
                if deep_price:
                    price = float(deep_price.group(1))
                    logger.info(f"Prezzo trovato via deep JSON search: {price}")

        # 2. Cerca pattern generici in tutti gli altri script (se non ancora trovato)
        if not price:
            for pattern in price_patterns:
                match = re.search(pattern, script_content)
                if match:
                    val = match.group(1)
                    if "€" in val or "," in val:
                        price = clean_price(val)
                    else:
                        price = float(val)
                    
                    if price:
                        logger.info(f"Prezzo trovato via JSON generico ({pattern}): {price}")
                        break

    return price, availability, condition

def parse_image(soup):
    """Estrae URL immagine principale con fallback."""
    selectors = [
        {"id": "landingImage"},
        {"id": "main-image"},
        {"id": "imgBlkFront"},
        {"class": "a-dynamic-image"}
    ]
    
    for sel in selectors:
        tag = soup.find(**sel)
        if tag and tag.get('src'):
            src = tag['src']
            if "data:image" not in src: # Salta placeholder base64
                return src
            if tag.get('data-old-hires'):
                return tag['data-old-hires']
                
    return None

def parse_rating(soup):
    """Estrae rating medio."""
    # Il rating spesso è in un'icona con testo alt
    rating_tag = soup.find("span", {"class": "a-icon-alt"}) or soup.find("i", class_=re.compile(r"a-star-"))
    if rating_tag:
        rating_text = rating_tag.get_text(strip=True)
        try:
            # Cerca il primo numero decimale (es: 4.5 o 4,5)
            match = re.search(r"(\d[.,]\d)", rating_text)
            if match:
                return float(match.group(1).replace(",", "."))
        except (ValueError, AttributeError):
            pass
    return None

def parse_details(soup):
    """Estrae dettagli prodotto (tabella)."""
    details = []
    # Amazon usa diverse tabelle per i dettagli a seconda della categoria
    details_selectors = [
        "table.a-normal.a-spacing-micro",
        "div#productDetails_techSpec_section_1 table",
        "table#productDetails_techSpec_section_1"
    ]
    
    for sel in details_selectors:
        details_section = soup.select_one(sel)
        if details_section:
            rows = details_section.find_all("tr")
            for row in rows:
                try:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        key = cols[0].get_text(strip=True)
                        value = cols[1].get_text(strip=True)
                        details.append({key: value})
                    else:
                        th = row.find("th")
                        td = row.find("td")
                        if th and td:
                            details.append({th.get_text(strip=True): td.get_text(strip=True)})
                except Exception:
                    continue
            if details: break # Esci se abbiamo trovato qualcosa
            
    return details
    
def parse_category(soup):
    """Estrae la categoria del prodotto dai breadcrumbs."""
    breadcrumb_tag = soup.find("div", id="wayfinding-breadcrumbs_container")
    if breadcrumb_tag:
        items = breadcrumb_tag.find_all("li")
        if items:
            # Di solito l'ultima o la penultima voce è la categoria più specifica
            # Ma prendiamo la prima o la seconda per una categoria più generale e pulita
            for item in items:
                cat = item.get_text(strip=True)
                if cat and cat != "›":
                    return cat
    return None

def parse_coupon(soup):
    """Estrae informazioni coupon."""
    coupon = False
    coupon_value = None

    # Amazon indica i coupon con varie classi
    coupon_selectors = [
        "i.newCouponBadge",
        "span.vcp-coupon-text",
        "label[for*='coupon']",
        "span.promoPriceBlockMessage"
    ]
    
    for sel in coupon_selectors:
        coupon_tag = soup.select_one(sel)
        if coupon_tag:
            logger.info(f"Possibile coupon trovato con selettore: {sel}")
            container = coupon_tag.find_parent("span") or coupon_tag.parent
            text = container.get_text(strip=True)
            # Cerca pattern come "Risparmia 2,00€" o "Sconto 10%"
            val_match = re.search(r"(\d+[.,]?\d*)\s*(?:€|%)", text)
            if val_match:
                coupon = True
                coupon_value = val_match.group(1).replace(",", ".")
                logger.info(f"Valore coupon estratto: {coupon_value}")
                return True, float(coupon_value)
            else:
                coupon = True
                
    return coupon, None

def fetch_product_data(url, mode="classic", max_retries=7, initial_delay=3):
    """Orchestratore dello scraping migliorato."""
    logger.info(f"Inizio scraping per URL: {url} (Modo: {mode})")

    asin = get_asin_from_url(url)
    if not asin:
        logger.error("ASIN non trovato nell'URL")
        raise ValueError("ASIN non trovato nell'URL")
    
    logger.info(f"ASIN trovato: {asin}")
    
    # Recupera impostazioni proxy dal database
    proxies = None
    try:
        settings_col = get_settings_collection()
        settings = settings_col.find_one({"type": "scraper_config"})
        if settings and settings.get("use_proxy"):
            proxy_url = settings.get("proxy_url")
            proxy_user = settings.get("proxy_user")
            proxy_pass = settings.get("proxy_pass")
            
            if proxy_url:
                if proxy_user and proxy_pass:
                    # Formato: http://user:pass@host:port
                    auth_proxy = proxy_url.replace("://", f"://{proxy_user}:{proxy_pass}@")
                    proxies = {"http": auth_proxy, "https": auth_proxy}
                else:
                    proxies = {"http": proxy_url, "https": proxy_url}
                logger.info(f"Utilizzo proxy configurato: {proxy_url}")
    except Exception as e:
        logger.error(f"Errore nel recupero della configurazione proxy: {e}")

    soup = get_page_content(url, max_retries, initial_delay, proxies=proxies)
    if not soup:
         raise Exception("Impossibile recuperare il contenuto della pagina dopo ripetuti tentativi")

    # Cerchiamo di identificare se siamo su una pagina prodotto valida
    # A volte id="dp" non c'è, proviamo altri contenitori comuni
    main_container = soup.find(id="dp") or soup.find(id="ppd") or soup.find(id="centerCol")
    
    if not main_container:
        # Se non troviamo il contenitore ma abbiamo il soup, proviamo lo stesso a estrarre i dati fondamentali dal soup globale
        logger.warning("Contenitore principale non trovato, procedo con estrazione globale")
        main_container = soup

    title = parse_title(main_container)
    price, condition = parse_price_and_condition(main_container)
    image_url = parse_image(main_container)
    rating = parse_rating(main_container)
    details = parse_details(main_container)
    category = parse_category(soup) # Usa soup globale per i breadcrumbs
    coupon, coupon_value = parse_coupon(main_container)

    # 4. JSON parsing fallback if requested or if CSS fails
    if mode == "json" or (price is None and mode == "classic"):
        logger.info(f"Eseguo parsing JSON (modalità: {mode})...")
        json_price, json_avail, json_cond = parse_data_from_json(soup)
        if json_price:
            price = json_price
            availability = json_avail
            condition = json_cond
            logger.info(f"Dati recuperati con successo tramite JSON: {price}")

    extraction_date = datetime.now().isoformat()
    
    # Se il titolo non è disponibile e non c'è prezzo, probabilmente siamo stati bloccati o il layout è radicalmente diverso
    if title == "Titolo non disponibile" and price is None:
        logger.error("Data extraction failed: layout unknown or block suspected")
        # Analisi diagnostica breve
        if "captcha" in soup.text.lower():
            raise Exception("Accesso bloccato da CAPTCHA")
        raise Exception("Impossibile estrarre dati vitali dal prodotto")

    logger.info(f"Scraping completato: {title[:30]}... Prezzo: {price}")

    return {
        "asin": asin,
        "title": title,
        "price": price,
        "condition": condition,
        "image_url": image_url,
        "rating": rating,
        "availability": "Disponibile" if condition != "Non disponibile" else "Non disponibile",
        "details": details,
        "category": category,
        "extraction_date": extraction_date,
        "insertion_date": extraction_date,
        "price_history": [{"date": extraction_date, "price": price}] if price else [],
        "coupon": coupon,
        "coupon_value": coupon_value
    }
