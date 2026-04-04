import os
import requests
import asyncio
from bson import ObjectId
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from app.db import get_db
from app.services.article_service import generate_seo_article

def get_amazon_product_data(asin):
    """Scrapes product data from Amazon (simple version)."""
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = f"https://www.amazon.it/dp/{asin}"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Amazon Scraper: Received status {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Title Selectors
        title = soup.find("span", {"id": "productTitle"}) or \
                soup.find("h1", {"id": "title"})
        
        # Image Selectors
        image = soup.find("img", {"id": "landingImage"}) or \
                soup.find("img", {"id": "imgBlkFront"}) or \
                soup.find("img", {"class": "a-dynamic-image"})
        
        # Price Selectors
        price_whole = soup.find("span", {"class": "a-price-whole"})
        price_fraction = soup.find("span", {"class": "a-price-fraction"})
        
        price_str = "N/A"
        if price_whole:
            price_str = price_whole.get_text(strip=True)
            if price_fraction:
                price_str += f",{price_fraction.get_text(strip=True)}"
        
        return {
            "title": title.get_text(strip=True) if title else "Prodotto Amazon",
            "image_url": image["src"] if image and image.has_attr("src") else f"https://placehold.co/600x400?text=Amazon+Product",
            "price": price_str,
            "url": f"https://www.amazon.it/dp/{asin}?tag={os.getenv('AFFILIATE_TAG', 'amazonit026-21')}"
        }
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
        return None

async def generate_article_task(article_id: str):
    """
    Background task to generate an article.
    Updated to use existing product data from DB instead of fresh scraping.
    """
    db = get_db()
    article = db.articles.find_one({"_id": ObjectId(article_id)})
    if not article:
        return

    # Update status to generating
    db.articles.update_one({"_id": ObjectId(article_id)}, {"$set": {"status": "generating"}})

    try:
        is_multi = "asins" in article and bool(article["asins"])
        
        if is_multi:
            products_cursor = db.products.find({"asin": {"$in": article["asins"]}})
            products_data = list(products_cursor)
            if not products_data:
                raise Exception(f"Nessun prodotto trovato per la lista di ASIN")
                
            content = await generate_seo_article(
                keyword=article["keyword"],
                product_data=None,
                products_data=products_data
            )
            
            db.articles.update_one(
                {"_id": ObjectId(article_id)},
                {"$set": {
                    "title": content["title"],
                    "content_html": content["content_html"],
                    "meta_description": content["meta_description"],
                    "slug": content.get("slug") or article["keyword"].lower().replace(' ', '-'),
                    "status": "published",
                    "published_at": datetime.utcnow().isoformat()
                }}
            )
            
        else:
            # 1. Fetch product data from the 'products' collection
            product_data = db.products.find_one({"asin": article["asin"]})
            
            if not product_data:
                raise Exception(f"Prodotto con ASIN {article['asin']} non trovato nella collezione 'products'")

            # 2. Generate content with AI
            content = await generate_seo_article(
                keyword=article["keyword"],
                product_data=product_data,
                products_data=None
            )
            
            print(f"DEBUG: AI Content generated. Length: {len(content.get('content_html', ''))}")

            # 3. Save to DB
            db.articles.update_one(
                {"_id": ObjectId(article_id)},
                {"$set": {
                    "title": content["title"],
                    "content_html": content["content_html"],
                    "meta_description": content["meta_description"],
                    "slug": content.get("slug") or article["keyword"].lower().replace(' ', '-'),
                    "amazon_product_url": f"https://www.amazon.it/dp/{article['asin']}?tag={os.getenv('AFFILIATE_TAG', 'amazonit026-21')}",
                    "amazon_product_image_url": product_data.get("image_url"),
                    "amazon_product_price": str(product_data.get("price", "N/A")),
                    "status": "published",
                    "published_at": datetime.utcnow().isoformat()
                }}
            )
        
        print(f"Article {article_id} generated successfully!")

    except Exception as e:
        print(f"Error generating article {article_id}: {e}")
        db.articles.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {"status": "failed", "error": str(e)}}
        )
