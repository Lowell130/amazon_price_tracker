import requests
import re
import json
import time
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_random_headers():
    ua = UserAgent()
    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

def test_url(url):
    print(f"\n--- Analisi URL: {url} ---")
    session = requests.Session()
    # "Warm up" hit the home page
    try:
        session.get("https://www.amazon.it/", headers=get_random_headers(), timeout=10)
        time.sleep(random.uniform(2, 5))
        
        response = session.get(url, headers=get_random_headers(), timeout=15)
        if response.status_code != 200:
            print(f"Errore HTTP: {response.status_code}")
            return

        if "captcha" in response.text.lower():
            print("Rilevato CAPTCHA - Accesso bloccato.")
            return

        scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', response.text)
        
        found = False
        for s in scripts:
            if "twister-js-init-dpx-data" in s:
                print("[TROVATO] script: twister-js-init-dpx-data")
                match = re.search(r'var dataToReturn = (\{.*?\});', s, re.DOTALL)
                if match:
                    json_data = match.group(1)
                    # Vediamo di estrarre la parte dei prezzi
                    print(f"Anteprima Dati JSON:\n{json_data[:1500]}...")
                    found = True
            
            # Cerca anche oggetti prezzo sparsi
            price_match = re.search(r'"priceAmount":\s*(\d+\.?\d*)', s)
            if price_match:
                print(f"[TROVATO] Prezzo nel JSON: {price_match.group(1)}")
                found = True

        if not found:
            print("Nessun dato JSON specifico trovato, ma la pagina è stata caricata.")
            # Stampiamo i primi 500 caratteri per vedere cosa abbiamo preso
            print(f"Preview HTML: {response.text[:500]}")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    urls = [
        "https://www.amazon.it/dp/B0DV4X1ZSL",
        "https://www.amazon.it/dp/B0DJDT9XH4"
    ]
    test_url(urls[0])
