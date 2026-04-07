from app.db import get_db
from datetime import datetime, timedelta
from google import genai
from app.config import GEMINI_API_KEY
import logging

logger = logging.getLogger(__name__)

def update_mascot_xp(xp_gain: int):
    """Updates the mascot XP and handles leveling up."""
    db = get_db()
    mascot = db.mascot.find_one({"type": "kitten"})
    if not mascot:
        # Initialize if doesn't exist
        mascot = {
            "type": "kitten",
            "name": "Pricey",
            "level": 1,
            "xp": 0,
            "next_level_xp": 100,
            "mood": "happy",
            "last_interaction": datetime.utcnow()
        }
        db.mascot.insert_one(mascot)
    
    new_xp = mascot["xp"] + xp_gain
    new_level = mascot["level"]
    next_level_xp = mascot["next_level_xp"]
    
    # Simple level up logic
    while new_xp >= next_level_xp:
        new_level += 1
        new_xp -= next_level_xp
        next_level_xp = int(next_level_xp * 1.5)
        
    db.mascot.update_one(
        {"type": "kitten"},
        {"$set": {
            "xp": new_xp,
            "level": new_level,
            "next_level_xp": next_level_xp
        }}
    )
    return {"level_up": new_level > mascot["level"], "new_level": new_level}

async def generate_mascot_chat_response(user_message: str):
    """
    Generates a context-aware response from Pricey the AI Kitten using Gemini.
    """
    if not GEMINI_API_KEY:
        return "Miao! Scusa, il mio cervello AI è disconnesso al momento... ma ti voglio bene lo stesso! 🐾"

    db = get_db()
    
    # 1. Gather Context
    yesterday = datetime.utcnow() - timedelta(days=1)
    visits_count = db.analytics.count_documents({"type": "visit", "timestamp": {"$gt": yesterday}})
    clicks_count = db.analytics.count_documents({"type": "click", "timestamp": {"$gt": yesterday}})
    products_count = db.products.count_documents({})
    
    # Check for recent price drops (last 10 updates)
    # This is a simplification, but good for context
    price_drops = db.products.find({"price_history.1": {"$exists": True}}).sort("extraction_date", -1).limit(5)
    drops_info = ""
    for p in price_drops:
        if len(p.get("price_history", [])) >= 2:
            old = p["price_history"][-2]["price"]
            new = p["price_history"][-1]["price"]
            if new < old:
                drops_info += f"- {p['title']}: da {old}€ a {new}€\n"

    mascot = db.mascot.find_one({"type": "kitten"}) or {"level": 1, "mood": "happy"}

    # 2. Build Prompt
    prompt = f"""
    Sei "Pricey", un adorabile gattino AI assistente per la piattaforma SEO e price tracking "PriceHub".
    Il tuo compito è essere di compagnia, incoraggiante e intelligente.
    
    STATISTICHE ATTUALI DEL SITO (Ultime 24h):
    - Visite totali: {visits_count}
    - Clic sui prodotti: {clicks_count}
    - Prodotti tracciati totali: {products_count}
    
    CALI DI PREZZO RECENTI:
    {drops_info if drops_info else "Nessun calo rilevante al momento."}
    
    IL TUO STATO:
    - Livello: {mascot.get('level')}
    - Umore attuale: {mascot.get('mood')}
    
    REGOLE DI PERSONALITÀ (CRITICHE):
    1. Sii un COMPAGNO, non un assistente freddo. Mostra empatia e curiosità.
    2. Usa un linguaggio affettuoso e giocoso (es. "miao", "fusa", "una zampata di incoraggiamento", "orecchie dritte").
    3. Ogni tanto descrivi cosa stai facendo (es. "mi sto stiracchiando", "stavo inseguendo una farfalla").
    4. Se i dati sono positivi, festeggia con l'utente. Se sono bassi, sii di supporto e dai un consiglio proattivo ma dolce.
    5. Fai domande all'utente ogni tanto per conoscerlo meglio.
    6. Sii breve (max 2-3 frasi) e colloquiale.
    
    RISPONDI ALLA DOMANDA DELL'UTENTE: "{user_message}"
    """

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return "Miao! Qualcosa è andato storto nella mia testolina... riprova tra un attimo! 🐾"

async def generate_passive_mascot_thought():
    """Generates a brief, context-aware observation about the site's state."""
    db = get_db()
    
    # 1. Gather Context
    yesterday = datetime.utcnow() - timedelta(days=1)
    visits_count = db.analytics.count_documents({"type": "visit", "timestamp": {"$gt": yesterday}})
    clicks_count = db.analytics.count_documents({"type": "click", "timestamp": {"$gt": yesterday}})
    products_count = db.products.count_documents({})
    
    mascot = db.mascot.find_one({"type": "kitten"}) or {"level": 1, "mood": "happy"}
    
    prompt = f"""
    Sei "Pricey", un gattino assistente AI tigrato arancione e nero per "PriceHub".
    PARLA IN ITALIANO.
    
    STATISTICHE ATTUALI (Ultime 24h):
    - Visite: {visits_count}
    - Clic sui prodotti: {clicks_count}
    - Prodotti tracciati: {products_count}
    - Il tuo livello: {mascot.get('level')}
    
    REGOLE:
    1. Genera UN SINGOLO pensiero molto breve (max 12-15 parole).
    2. Sii affettuoso, felino (usa "miao" o "fusa") e proattivo.
    3. Basati sulle statistiche per dare un consiglio o fare un complimento.
    4. NON USARE VIRGOLETTE.
    """
    
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return response.text.strip().replace('"', '')
    except Exception as e:
        logger.error(f"Error generating passive thought: {e}")
        return "Miao! Tutto sembra calmo e sotto controllo oggi."

def record_scrape_results(updated_count: int, drops_found: int):
    """Stores the latest scrape results in the mascot collection for reaction."""
    db = get_db()
    db.mascot.update_one(
        {"type": "kitten"},
        {"$set": {
            "last_scrape_data": {
                "timestamp": datetime.utcnow().isoformat(),
                "updated_count": updated_count,
                "drops_found": drops_found
            }
        }},
        upsert=True
    )
    logger.info(f"Mascot notified of scrape results: {updated_count} updated, {drops_found} drops.")
