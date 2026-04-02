import requests
import re
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_random_headers():
    ua = UserAgent()
    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.it/",
        "Connection": "keep-alive"
    }

def test_url(url):
    print(f"\n--- Analisi URL: {url[:60]}... ---")
    headers = get_random_headers()
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Errore HTTP: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Cerca blocchi script interessanti
        scripts = soup.find_all("script")
        found_data = []

        # Pattern 1: twister-js-init-dpx-data
        for s in scripts:
            if s.string and "twister-js-init-dpx-data" in s.string:
                print(f"[TROVATO] script: twister-js-init-dpx-data")
                # Estrai il blocco JSON che inizia con var dataToReturn = { ...
                match = re.search(r'var dataToReturn = (\{.*?\});', s.string, re.DOTALL)
                if match:
                    try:
                        # Pulizia minima per rendere il JS un JSON valido (spesso serve a scopi demo)
                        json_str = match.group(1)
                        # Molti di questi non sono JSON "puri" ma oggetti JS.
                        # Per ora stampiamo i primi 1000 caratteri puliti
                        print(f"Estratto JSON (anteprima):\n{json_str[:1000]}...")
                    except Exception as je:
                        print(f"Errore parsing: {je}")

            # Pattern 3: Oggetti prezzo diretti (Regex)
            # Cerca pattern come "priceAmount": 12.34
            price_matches = re.findall(r'"(priceAmount|displayPrice|amount)":\s*["\']?(\d+[.,]\d+|\d+)["\']?', s.string if s.string else "")
            for pm in price_matches:
                print(f"[TROVATO] {pm[0]}: {pm[1]}")

        if not found_data:
            print("Nessun dato JSON rilevante trovato nei tag <script>.")
            if "captcha" in response.text.lower():
                print("Rilevato CAPTCHA - Accesso bloccato.")
        else:
            for item in found_data:
                print(f"Dato: {item}")

    except Exception as e:
        print(f"Errore durante la richiesta: {e}")

if __name__ == "__main__":
    urls = [
        "https://www.amazon.it/dp/B0DV4X1ZSL",
        "https://www.amazon.it/dp/B0DJDT9XH4"
    ]
    for u in urls:
        test_url(u)
