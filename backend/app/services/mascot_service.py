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

async def generate_mascot_chat_response(user_message: str, user_name: str = "Amico"):
    """
    Generates a context-aware response from Pricey the AI Kitten using Gemini.
    """
    if not GEMINI_API_KEY:
        return f"Miao {user_name}! Scusa, il mio cervello AI è disconnesso al momento... ma ti voglio bene lo stesso! 🐾"

    db = get_db()
    
    # 1. Gather Context
    yesterday = datetime.utcnow() - timedelta(days=1)
    visits_count = db.analytics.count_documents({"type": "visit", "timestamp": {"$gt": yesterday}})
    clicks_count = db.analytics.count_documents({"type": "click", "timestamp": {"$gt": yesterday}})
    products_count = db.products.count_documents({})
    
    # Check for recent price drops (last 10 updates)
    price_drops = db.products.find({"price_history.1": {"$exists": True}}).sort("extraction_date", -1).limit(10)
    drops_info = ""
    
    def parse_price(p_str):
        try:
            return float(p_str.replace('€', '').replace('.', '').replace(',', '.').strip())
        except:
            return None

    for p in price_drops:
        if len(p.get("price_history", [])) >= 2:
            old_val = parse_price(str(p["price_history"][-2].get("price", "0")))
            new_val = parse_price(str(p["price_history"][-1].get("price", "0")))
            if old_val and new_val and new_val < old_val:
                drops_info += f"- {p['title'][:50]}...: da {p['price_history'][-2]['price']}€ a {p['price_history'][-1]['price']}€\n"

    mascot = db.mascot.find_one({"type": "kitten"}) or {"level": 1, "mood": "happy"}

    # 2. Build Prompt
    prompt = f"""
    Sei "Pricey", un adorabile gattino AI assistente per la piattaforma SEO e price tracking "PriceHub".
    Il tuo compito è essere di compagnia, incoraggiante e intelligente.
    L'utente con cui stai parlando si chiama: {user_name}
    
    STATISTICHE ATTUALI DEL SITO (Ultime 24h):
    - Visite totali: {visits_count}
    - Clic sui prodotti: {clicks_count}
    - Prodotti tracciati totali: {products_count}
    
    CALI DI PREZZO RECENTI RILEVATI:
    {drops_info if drops_info else "Nessun calo rilevante al momento."}
    
    IL TUO STATO:
    - Livello: {mascot.get('level')}
    - Umore attuale: {mascot.get('mood')}
    
    REGOLE DI PERSONALITÀ (CRITICHE):
    1. Sii un COMPAGNO, non un assistente freddo. Mostra empatia e curiosità.
    2. Chiama l'utente per nome ({user_name}) ogni volta che ti sembra naturale e amichevole.
    3. Usa un linguaggio affettuoso e giocoso (es. "miao", "fusa", "una zampata di incoraggiamento", "orecchie dritte").
    4. Ogni tanto descrivi cosa stai facendo (es. "mi sto stiracchiando", "stavo inseguendo una farfalla").
    5. Se ci sono cali di prezzo, menziona specificamente uno o due prodotti dai dati sopra per mostrare che sei attento!
    6. Se i dati sono positivi, festeggia con l'utente. Se sono bassi, sii di supporto e dai un consiglio proattivo ma dolce.
    7. Sii breve (max 2-3 frasi) e colloquiale.
    
    RISPONDI ALLA DOMANDA DI {user_name}: "{user_message}"
    """

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Miao {user_name}! Qualcosa è andato storto nella mia testolina... riprova tra un attimo! 🐾"

async def generate_passive_mascot_thought():
    """Generates a brief, context-aware observation about the site's state."""
    db = get_db()
    
    # 1. Gather Context
    yesterday = datetime.utcnow() - timedelta(days=1)
    visits_count = db.analytics.count_documents({"type": "visit", "timestamp": {"$gt": yesterday}})
    clicks_count = db.analytics.count_documents({"type": "click", "timestamp": {"$gt": yesterday}})
    products_count = db.products.count_documents({})
    
    # Get a couple of recent price drops for the thought
    recent_drops = list(db.products.find({"price_history.1": {"$exists": True}}).sort("extraction_date", -1).limit(3))
    drop_hint = ""
    if recent_drops:
        drop_hint = f"Ultimi prodotti in calo: {', '.join([d['title'][:30] for d in recent_drops])}"

    mascot = db.mascot.find_one({"type": "kitten"}) or {"level": 1, "mood": "happy"}
    
    prompt = f"""
    Sei "Pricey", un gattino assistente AI tigrato arancione e nero per "PriceHub".
    PARLA IN ITALIANO.
    
    STATISTICHE ATTUALI (Ultime 24h):
    - Visite: {visits_count}
    - Clic: {clicks_count}
    - Prodotti: {products_count}
    - {drop_hint}
    
    REGOLE:
    1. Genera UN SINGOLO pensiero molto breve (max 12-15 parole).
    2. Sii affettuoso, felino e proattivo.
    3. Se ci sono stati cali di prezzo recenti, prova a menzionarne uno brevemente.
    4. Basati sulle statistiche per dare un consiglio o fare un complimento.
    5. NON USARE VIRGOLETTE.
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

async def get_site_context():
    """Gathers deep site context for the mascot."""
    db = get_db()
    yesterday = datetime.utcnow() - timedelta(days=1)
    two_days_ago = datetime.utcnow() - timedelta(days=2)
    
    context = {
        "visits_24h": db.analytics.count_documents({"type": "visit", "timestamp": {"$gt": yesterday}}),
        "clicks_24h": db.analytics.count_documents({"type": "click", "timestamp": {"$gt": yesterday}}),
        "total_products": db.products.count_documents({}),
        "total_articles": db.articles.count_documents({"status": "published"}),
        "stale_products": db.products.count_documents({"extraction_date": {"$lt": two_days_ago.isoformat()}}),
        "latest_article": db.articles.find_one({"status": "published"}, sort=[("published_at", -1)])
    }
    
    # Simple list of recent drops
    recent_drops = list(db.products.find({"price_history.1": {"$exists": True}}).sort("extraction_date", -1).limit(5))
    context["recent_drops_titles"] = [d["title"][:50] for d in recent_drops]
    
    return context

async def generate_proactive_insight():
    """Generates a proactive tip or alert based on site state."""
    ctx = await get_site_context()
    
    prompt = f"""
    Sei "Pricey", il gattino assistente di PriceHub. Parla in modo autonomo e proattivo.
    DATI SITO:
    - Articoli pubblicati: {ctx['total_articles']}
    - Prodotti totali: {ctx['total_products']}
    - Prodotti con prezzi vecchi (>48h): {ctx['stale_products']}
    - Click ultime 24h: {ctx['clicks_24h']}
    - Visite ultime 24h: {ctx['visits_24h']}
    
    REGOLE:
    1. Scegli UN SOLO problema o opportunità dai dati sopra.
    2. Genera un messaggio breve (max 20 parole) e amichevole.
    3. Se ci sono prodotti vecchi, suggerisci di aggiornarli.
    4. Se ci sono pochi articoli, suggerisci di scriverne uno nuovo.
    5. Se le statistiche sono ottime, festeggia!
    6. Sii un compagno fedele che "vive" il sito insieme all'admin.
    """
    
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return response.text.strip().replace('"', '')
    except Exception:
        return None

async def get_autonomous_action():
    """Decides if the mascot should perform an autonomous action."""
    db = get_db()
    mascot = db.mascot.find_one({"type": "kitten"}) or {}
    last_action = mascot.get("last_autonomous_action_time")
    
    # Rate limit: 1 autonomous action every 1 hour (3600 seconds)
    if last_action and (datetime.utcnow() - last_action).total_seconds() < 3600:
        return None

    ctx = await get_site_context()
    possible_actions = []
    
    # Action Type 1: Stale Products (Price Updates)
    if ctx.get("stale_products", 0) > 0:
        stale_prod = db.products.find_one(
            {"extraction_date": {"$lt": (datetime.utcnow() - timedelta(days=2)).isoformat()}},
            sort=[("extraction_date", 1)]
        )
        if stale_prod:
            possible_actions.append({"type": "update_price", "asin": stale_prod["asin"], "title": stale_prod["title"]})

    # Action Type 2: Missing Articles
    if ctx.get("total_products", 0) > 0:
        # Simple check: find a product that doesn't have a corresponding article
        all_asins = [p["asin"] for p in db.products.find({}, {"asin": 1}).limit(50)]
        for asin in all_asins:
            if not db.articles.find_one({"$or": [{"asin": asin}, {"asins": asin}]}):
                prod = db.products.find_one({"asin": asin})
                if prod:
                    possible_actions.append({"type": "generate_article", "asin": asin, "title": prod["title"]})
                    break # Just take the first one found

    if possible_actions:
        import random
        return random.choice(possible_actions)

    return None

def record_mascot_notification(message: str):
    """Stores a pending notification for the mascot to show to the admin."""
    db = get_db()
    db.mascot.update_one(
        {"type": "kitten"},
        {"$set": {
            "pending_notification": message,
            "last_autonomous_action_time": datetime.utcnow()
        }}
    )

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
