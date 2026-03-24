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
    Scrivi un articolo di recensione professionale e accattivante in formato HTML.
    
    Keyword di riferimento (per focus SEO): "{keyword}"
    
    Dati Reali del Prodotto (USA QUESTI DATI):
    - Nome Completo: {product_data.get('title')}
    - Prezzo Attuale: {product_data.get('price')}€
    - Caratteristiche Tecniche: {features_str}
    
    ISTRUZIONI CRITICHE:
    1. TITOLO ARTICOLO: Non limitarti alla keyword. Crea un titolo editoriale forte che includa il Nome Completo del prodotto. 
       Esempio: "Recensione [Nome Prodotto]: [Slogan o Beneficio Principale]".
    2. CONTENUTO: Usa tag HTML semantici (<h1>, <h2>, <p>, <ul>, <strong>).
    3. CALL TO ACTION: Inserisci il placeholder {{AMAZON_BUTTON}} dove opportuno.
    4. LINK: Se inserisci link nel testo, usa href="{{AMAZON_LINK}}".
    5. PREZZO DINAMICO: Non scrivere mai il prezzo reale come cifra statica nel testo (es. "Costa 49€"). 
       Usa SEMPRE il placeholder {{CURRENT_PRICE}} seguìto dal simbolo € (es. "Ora disponibile a {{CURRENT_PRICE}}€").
    6. COERENZA LOGICA: Focalizzati sulle caratteristiche tecniche, la qualità e l'utilità del prodotto. Evita di basare l'intera recensione esclusivamente sul fatto che il prezzo sia "un affare incredibile", perché il prezzo potrebbe variare. Lascia che sia il box di analisi dinamica a gestire i consigli sull'opportunità di acquisto.
    7. NESSUN Altro PLACEHOLDER: Non scrivere mai "N/A", "Non disponibile" o simili. Se un dato manca, omettilo.
    8. FORMATO: Ritorna SOLO JSON.
    
    Ritorna SOLO un JSON con questa struttura:
    {{
        "title": "Titolo Editoriale Accattivante",
        "slug": "url-amichevole-basato-sul-prodotto",
        "meta_description": "Descrizione 150-160 char ottimizzata",
        "content_html": "Corpo articolo HTML ricco e formattato"
    }}
    Ritorna solo l'oggetto JSON, senza markdown blocks.
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
