from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
import re
from typing import List
from bson import ObjectId
from datetime import datetime
from app.db import get_db
from app.schemas import ArticleModel, ArticleTrigger
from app.dependencies import admin_required
from app.services.tasks import generate_article_task  # Renamed from generate_article_flow

router = APIRouter(prefix="/api", tags=["articles"])

# ... (public endpoints remain same)

from pydantic import BaseModel
class EnhanceKeywordRequest(BaseModel):
    keyword: str

@router.post("/admin/articles/enhance-keyword", status_code=200)
async def enhance_seo_keyword_api(
    data: EnhanceKeywordRequest,
    admin: dict = Depends(admin_required)
):
    """Uses AI to turn a basic keyword into an engaging SEO title."""
    from app.services.article_service import enhance_seo_keyword
    enhanced = await enhance_seo_keyword(data.keyword)
    return {"keyword": enhanced}

@router.post("/admin/articles/trigger", status_code=201)
async def trigger_article_generation(
    data: ArticleTrigger, 
    background_tasks: BackgroundTasks,
    admin: dict = Depends(admin_required)
):
    """Triggers the async generation of an article using FastAPI BackgroundTasks."""
    db = get_db()
    
    # Check if already running or already published
    search_query = {}
    if data.asins:
        search_query = {"asins": data.asins, "status": {"$in": ["queued", "generating", "published"]}}
    else:
        search_query = {"asin": data.asin, "status": {"$in": ["queued", "generating", "published"]}}

    existing = db.articles.find_one(search_query)
    if existing:
        return {"id": str(existing["_id"]), "status": existing.get("status", "already_exists")}

    new_article = {
        "keyword": data.keyword,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat()
    }
    if data.asins:
        new_article["asins"] = data.asins
    else:
        new_article["asin"] = data.asin
    
    res = db.articles.insert_one(new_article)
    article_id = str(res.inserted_id)
    
    # Launch Background Task (integrated in FastAPI)
    background_tasks.add_task(generate_article_task, article_id)
    
    return {"id": article_id, "status": "queued"}

# PUBLIC ENDPOINTS

@router.get("/articles", response_model=List[ArticleModel])
async def get_public_articles():
    """Returns all published articles for the blog, enriched with current product data."""
    db = get_db()
    cursor = db.articles.find({"status": "published"}).sort("published_at", -1)
    articles = list(cursor)
    
    if not articles:
        return []

    # Get all ASINs to fetch product data in bulk
    asins_set = set()
    for a in articles:
        if "asin" in a and a["asin"]:
            asins_set.add(a["asin"])
        if "asins" in a and a["asins"]:
            asins_set.update(a["asins"])
            
    products = {p["asin"]: p for p in db.products.find({"asin": {"$in": list(asins_set)}})}

    enriched_articles = []
    for doc in articles:
        doc["id"] = str(doc["_id"])
        
        # Enrich with current product data if available
        if doc.get("asins"):
            doc_products = []
            for asin in doc["asins"]:
                if asin in products:
                    product_doc = products[asin].copy()
                    if "_id" in product_doc:
                        del product_doc["_id"]
                    doc_products.append(product_doc)
            doc["products"] = doc_products
            if doc_products: # set hero image and price from first product just in case
                doc["amazon_product_price"] = str(doc_products[0].get("price", doc.get("amazon_product_price", "N/A")))
                doc["amazon_product_image_url"] = doc_products[0].get("image_url", doc.get("amazon_product_image_url"))
        elif doc.get("asin"):
            asin = doc.get("asin")
            if asin in products:
                product_doc = products[asin].copy()
                # Sync price and image
                doc["amazon_product_price"] = str(product_doc.get("price", doc.get("amazon_product_price")))
                doc["amazon_product_image_url"] = product_doc.get("image_url", doc.get("amazon_product_image_url"))
                
                # Optional: Add full product object if needed by frontend
                # Remove _id for serialization
                if "_id" in product_doc:
                    del product_doc["_id"]
                doc["product"] = product_doc
            
        enriched_articles.append(ArticleModel(**doc))
        
    return enriched_articles

@router.get("/articles/{slug}", response_model=ArticleModel)
async def get_article_by_slug(slug: str):
    """Returns a single article by slug, enriched with real-time product data and analysis."""
    from app.services.analysis_service import analyze_product_price
    db = get_db()
    # Use case-insensitive search for resilience
    doc = db.articles.find_one({
        "slug": {"$regex": f"^{re.escape(slug)}$", "$options": "i"}, 
        "status": "published"
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Articolo non trovato")
    
    doc["id"] = str(doc["_id"])
    
    # Enrich with product data from 'products' collection
    if doc.get("asins"):
        products_cursor = db.products.find({"asin": {"$in": doc["asins"]}})
        doc_products = []
        for p in products_cursor:
            # Skip corrupted entries
            if not p.get("asin") or not p.get("title"):
                continue
            p_analysis = analyze_product_price(p)
            p_enriched = {**p, "analysis": p_analysis}
            if "_id" in p_enriched:
                del p_enriched["_id"]
            doc_products.append(p_enriched)
        
        # Riordina i prodotti in base all'ordine originale di asins
        ordered_products = []
        for a in doc["asins"]:
            found = next((dp for dp in doc_products if dp.get("asin") == a), None)
            if found:
                ordered_products.append(found)
        doc["products"] = ordered_products
    elif doc.get("asin"):
        product_doc = db.products.find_one({"asin": doc["asin"]})
        if product_doc:
            # Calculate analysis
            analysis = analyze_product_price(product_doc)
            # Merge global product data with analysis
            doc["product"] = {**product_doc, "analysis": analysis}
            # Remove _id from nested product for serialization
            if "_id" in doc["product"]:
                del doc["product"]["_id"]
    
    # Remove MongoDB internal _id before returning model
    if "_id" in doc:
        del doc["_id"]
            
    return ArticleModel(**doc)

# ADMIN ENDPOINTS

@router.get("/admin/articles", response_model=List[ArticleModel])
async def get_admin_articles(admin: dict = Depends(admin_required)):
    """Admin view: returns ALL articles including queued/failed."""
    db = get_db()
    cursor = db.articles.find({}).sort("created_at", -1)
    articles = list(cursor)
    
    if not articles:
        return []
        
    # Bulk fetch product images to avoid N+1 queries
    asins_set = set()
    for doc in articles:
        if doc.get("asin"):
            asins_set.add(doc["asin"])
        if doc.get("asins") and len(doc["asins"]) > 0:
            asins_set.add(doc["asins"][0]) # use first ASIN for cover image

    products_cursor = db.products.find({"asin": {"$in": list(asins_set)}}, {"asin": 1, "image_url": 1})
    products_map = {p["asin"]: p.get("image_url") for p in products_cursor}
    
    articles_list = []
    for doc in articles:
        doc["id"] = str(doc["_id"])
        # Use mapped image if available
        cover_asin = None
        if doc.get("asins") and len(doc["asins"]) > 0:
            cover_asin = doc["asins"][0]
        elif doc.get("asin"):
            cover_asin = doc.get("asin")
            
        if cover_asin and cover_asin in products_map:
            doc["product_image_url"] = products_map[cover_asin]
            
        articles_list.append(ArticleModel(**doc))
    return articles_list

@router.delete("/admin/articles/{article_id}")
async def delete_article(article_id: str, admin: dict = Depends(admin_required)):
    """Deletes an article."""
    db = get_db()
    res = db.articles.delete_one({"_id": ObjectId(article_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Articolo non trovato")
    return {"status": "deleted"}
