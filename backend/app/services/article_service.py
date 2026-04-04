import os
import json
import logging
from google import genai
from app.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

async def generate_seo_article(keyword: str, product_data: dict = None, products_data: list = None) -> dict:
    """
    Generates an SEO-optimized article using Gemini.
    Adapted for the Amazon Price Tracker project to support single and multi-product articles.
    """
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not configured")
        title_fallback = "Articolo su " + keyword
        if product_data:
            title_fallback = f"Recensione {product_data.get('title', keyword)}"
        return {
            "title": title_fallback,
            "meta_description": "API Key non configurata.",
            "content_html": "<p>Errore: GEMINI_API_KEY non configurata.</p>"
        }

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = ""
    
    if products_data and len(products_data) > 0:
        # Multi-product logic (Listicle / Comparison)
        products_info = ""
        for p in products_data:
            asin = p.get('asin', 'N/A')
            title = p.get('title', 'Prodotto sconosciuto')
            price = p.get('price', 'N/A')
            
            features_list = []
            if p.get('details'):
                for d in p['details']:
                    for k, v in d.items():
                        features_list.append(f"{k}: {v}")
            features_str = ", ".join(features_list[:5])
            
            products_info += f"- ASIN: {asin}\n  Nome: {title}\n  Prezzo: {price}€\n  Specifiche: {features_str}\n\n"

        prompt = f"""
        Sei un copywriter SEO esperto specializzato in product selection e listicle tech (es. "I migliori X del 2026").
        Scrivi il contenuto di un articolo comparativo e approfondito in formato HTML.
        
        Keyword principale: "{keyword}"
        
        Prodotti in esame:
        {products_info}
        
        MISSIONE SEO & STRUTTURA:
        1. GERARCHIA TITOLI: Non usare il tag <h1>. Inizia un'introduzione accattivante su "{keyword}".
        2. INTRODUZIONE: Scrivi 1-2 paragrafi includendo la keyword.
        3. RECENSIONI SINGOLE: Per ciascun prodotto elencato sopra crea un <h2> o <h3> col nome. Descrivi perché è in classifica, pregi e difetti.
        4. BOTTONE D'ACQUISTO (CRITICO): Alla fine di OGNI blocco prodotto, DEVI inserire esattamente la stringa {{{{AMAZON_BUTTON_TuoAsinQui}}}} per permettere al sistema di mostrare il box d'acquisto al posto corretto (sostituisci TuoAsinQui con l'ASIN reale del prodotto analizzato).
        5. CONCLUSIONE: Un paragrafo per tirare le somme.
        6. FORMATO RISPOSTA: Ritorna esclusivamente un oggetto JSON.
        
        Struttura JSON richiesta:
        {{
            "title": "Titolo editoriale che include il contesto o anno, es. I migliori X del 2026",
            "slug": "url-amichevole-basato-sulla-keyword",
            "meta_description": "Descrizione 150-160 caratteri ottimizzata per il CTR",
            "content_html": "Il corpo dell'articolo in HTML (solo intestazioni, p, ul, li, strong)"
        }}
        """
    else:
        # Single-product logic (Classic Review)
        features_list = []
        if product_data and product_data.get('details'):
            for d in product_data['details']:
                for k, v in d.items():
                    features_list.append(f"{k}: {v}")
        
        features_str = ", ".join(features_list[:10])

        prompt = f"""
        Sei un copywriter SEO esperto specializzato in recensioni tech e prodotti Amazon. 
        Scrivi il contenuto di un articolo di recensione professionale, approfondito e accattivante in formato HTML.
        
        Keyword principale: "{keyword}"
        
        Dati Prodotto:
        - Nome: {product_data.get('title') if product_data else keyword}
        - Prezzo attuale: {product_data.get('price') if product_data else 'N/A'}€
        - Specifiche: {features_str}
        
        MISSIONE SEO & STRUTTURA:
        1. GERARCHIA TITOLI (CRITICO): Non usare mai il tag <h1>. Inizia direttamente con <h2> per le sezioni principali e <h3> per i sottotitoli.
        2. INTRODUZIONE: Scrivi un'intro che catturi l'attenzione includendo la keyword principale nei primi due paragrafi.
        3. ANALISI TECNICA: Approfondisci le caratteristiche fornite, spiegando i benefici per l'utente, non solo l'elenco tecnico.
        4. PRO & CONTRO: Includi una sezione dedicata ai punti di forza e di debolezza del prodotto usando <ul>.
        5. USER EXPERIENCE: Immagina come viene utilizzato il prodotto nella vita reale.
        6. PREZZO DINAMICO: Usa {{{{CURRENT_PRICE}}}}€ per riferirti al prezzo attuale.
        7. CALL TO ACTION: Inserisci il placeholder {{{{AMAZON_BUTTON}}}} vicino alla fine o dopo i "Pro & Contro".
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
        config = genai.types.GenerateContentConfig(
            response_mime_type="application/json"
        )
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt,
            config=config
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
            "title": f"Articolo su {keyword}",
            "meta_description": "Errore durante la generazione AI.",
            "content_html": f"<div class='p-8 bg-red-50 text-red-600 rounded-2xl'><strong>Errore AI:</strong> {str(e)}<br><pre class='mt-4 text-xs bg-white p-4 rounded overflow-auto'>{text if 'text' in locals() else ''}</pre></div>"
        }

async def enhance_seo_keyword(keyword: str) -> str:
    """Uses Gemini to generate a much more engaging SEO title for a basic keyword."""
    if not GEMINI_API_KEY:
        return keyword
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""
    Sei un copywriter SEO esperto. L'utente ha fornito questa keyword di base: "{keyword}".
    Trasformala in un Titolo SEO altamente accattivante, perfetto per un Listicle o Guida all'Acquisto.
    Deve catturare l'attenzione e aumentare i click. Restuisci SOLO ed esclusivamente la stringa del nuovo titolo, niente virgolette aggiuntive o altre parole. Esempio: "I 10 Migliori Mouse Gaming del 2026: Guida Definitiva"
    """
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return response.text.strip().strip('"').strip("'")
    except Exception as e:
        logger.error(f"Error enhancing keyword: {e}")
        return keyword
