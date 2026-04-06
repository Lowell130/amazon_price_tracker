from fastapi import APIRouter, Response
from app.db import get_db
from app.config import BASE_URL
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime

router = APIRouter(tags=["seo"])

@router.get("/sitemap.xml", response_class=Response)
async def generate_sitemap():
    """
    Genera una sitemap dinamica in XML con articoli, prodotti e pagine statiche.
    """
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    db = get_db()

    def add_url(loc, lastmod=None, priority="0.5", changefreq="weekly"):
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = loc
        if lastmod:
            SubElement(url, "lastmod").text = lastmod
        else:
            SubElement(url, "lastmod").text = datetime.today().strftime("%Y-%m-%d")
        SubElement(url, "priority").text = priority
        SubElement(url, "changefreq").text = changefreq

    # --- PAGINE STATICHE ---
    add_url(f"{BASE_URL}/", priority="1.0", changefreq="daily")
    add_url(f"{BASE_URL}/products", priority="0.8", changefreq="daily")

    # --- ARTICOLI (BLOG) ---
    articles = db.articles.find({"status": "published"}, {"slug": 2, "updated_at": 1, "published_at": 1})
    for art in articles:
        if art.get("slug"):
            lastmod = art.get("published_at") or art.get("updated_at")
            if lastmod and isinstance(lastmod, str):
                lastmod = lastmod[:10]  # Prendi solo YYYY-MM-DD
            else:
                lastmod = datetime.today().strftime("%Y-%m-%d")
                
            add_url(f"{BASE_URL}/blog/{art['slug']}", lastmod=lastmod, priority="0.9", changefreq="monthly")

    # --- PRODOTTI ---
    products = db.products.find({}, {"asin": 1, "updated_at": 1})
    for prod in products:
        if prod.get("asin"):
            lastmod = prod.get("updated_at")
            if lastmod and isinstance(lastmod, str):
                lastmod = lastmod[:10]
            else:
                lastmod = datetime.today().strftime("%Y-%m-%d")
                
            add_url(f"{BASE_URL}/products/{prod['asin']}", lastmod=lastmod, priority="0.7", changefreq="weekly")

    # Converti in stringa XML
    xml_data = tostring(urlset, encoding="utf-8", method="xml")
    
    # Aggiungi l'intestazione XML
    xml_output = b'<?xml version="1.0" encoding="UTF-8"?>' + xml_data

    return Response(content=xml_output, media_type="application/xml")
