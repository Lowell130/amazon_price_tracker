import os
import json
import logging
from google import genai
from app.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

async def generate_seo_article(keyword: str, product_data: dict) -> dict:
    """
    Generates an SEO-optimized article using Gemini 2.0 Flash.
    Adapted for the Amazon Price Tracker project.
    """
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not configured")
        return {
            "title": f"Recensione {product_data.get('title', keyword)}",
            "meta_description": "API Key non configurata.",
            "content_html": "<p>Errore: GEMINI_API_KEY non configurata.</p>"
        }

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Extract features from 'details' if available
    features_list = []
    if product_data.get('details'):
        for d in product_data['details']:
            for k, v in d.items():
                features_list.append(f"{k}: {v}")
    
    features_str = ", ".join(features_list[:10]) # Limit to 10 features for prompt

    prompt = f"""
    Sei un copywriter SEO esperto specializzato in recensioni tech e prodotti Amazon. 
    Scrivi il contenuto di un articolo di recensione professionale, approfondito e accattivante in formato HTML.
    
    Keyword principale: "{keyword}"
    
    Dati Prodotto:
    - Nome: {product_data.get('title')}
    - Prezzo attuale: {product_data.get('price')}€
    - Specifiche: {features_str}
    
    MISSIONE SEO & STRUTTURA:
    1. GERARCHIA TITOLI (CRITICO): Non usare mai il tag <h1> (è già presente nella pagina). Inizia direttamente con <h2> per le sezioni principali e <h3> per i sottotitoli.
    2. INTRODUZIONE: Scrivi un'intro che catturi l'attenzione includendo la keyword principale nei primi due paragrafi.
    3. ANALISI TECNICA: Approfondisci le caratteristiche fornite, spiegando i benefici per l'utente, non solo l'elenco tecnico.
    4. PRO & CONTRO: Includi una sezione dedicata ai punti di forza e di debolezza del prodotto usando <ul>.
    5. USER EXPERIENCE: Immagina come viene utilizzato il prodotto nella vita reale (es. "Perfetto per chi lavora in mobilità" o "Ideale per sessioni di gaming prolungate").
    6. PREZZO DINAMICO: Usa {{CURRENT_PRICE}}€ per riferirti al prezzo attuale.
    7. CALL TO ACTION: Inserisci il placeholder {{AMAZON_BUTTON}} vicino alla fine o dopo i "Pro & Contro".
    8. FORMATO RISPOSTA: Ritorna esclusivamente un oggetto JSON.
    
    Struttura JSON richiesta:
    {{
        "title": "Titolo editoriale che include il prodotto e un beneficio",
        "slug": "url-amichevole-basato-sul-prodotto-e-keyword",
        "meta_description": "Descrizione 150-160 caratteri ottimizzata per il click-through rate",
        "content_html": "Il corpo dell'articolo in HTML (solo <h2>, <h3>, <p>, <ul>, <li>, <strong>)"
    }}
    """
    
    try:
        # Use sync call since we are in a worker or we can wrap it
        print(f"DEBUG: Generating content with model: gemini-3-flash-preview")
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        text = response.text.strip()
        print(f"DEBUG: Raw AI Response (first 100 chars): {text[:100]}...")
        
        # Robust JSON extraction
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        
        return json.loads(text)
    except Exception as e:
        logger.error(f"Error generating AI content: {e}")
        return {
            "title": f"Recensione {product_data.get('title', keyword)}",
            "meta_description": "Errore durante la generazione AI.",
            "content_html": f"<div class='p-8 bg-red-50 text-red-600 rounded-2xl'><strong>Errore AI:</strong> {str(e)}<br><pre class='mt-4 text-xs bg-white p-4 rounded overflow-auto'>{text if 'text' in locals() else ''}</pre></div>"
        }
