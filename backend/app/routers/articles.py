from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List
from bson import ObjectId
from datetime import datetime
from app.db import get_db
from app.schemas import ArticleModel, ArticleTrigger
from app.dependencies import admin_required
from app.services.tasks import generate_article_task  # Renamed from generate_article_flow

router = APIRouter(prefix="/api", tags=["articles"])

# ... (public endpoints remain same)

@router.post("/admin/articles/trigger", status_code=201)
async def trigger_article_generation(
    data: ArticleTrigger, 
    background_tasks: BackgroundTasks,
    admin: dict = Depends(admin_required)
):
    """Triggers the async generation of an article using FastAPI BackgroundTasks."""
    db = get_db()
    
    # Check if already running or already published
    existing = db.articles.find_one({"asin": data.asin, "status": {"$in": ["queued", "generating", "published"]}})
    if existing:
        return {"id": str(existing["_id"]), "status": existing.get("status", "already_exists")}

    new_article = {
        "asin": data.asin,
        "keyword": data.keyword,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat()
    }
    
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
    asins = [a["asin"] for a in articles if "asin" in a]
    products = {p["asin"]: p for p in db.products.find({"asin": {"$in": asins}})}

    enriched_articles = []
    for doc in articles:
        doc["id"] = str(doc["_id"])
        
        # Enrich with current product data if available
        asin = doc.get("asin")
        if asin in products:
            product_doc = products[asin]
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
    doc = db.articles.find_one({"slug": slug, "status": "published"})
    if not doc:
        raise HTTPException(status_code=404, detail="Articolo non trovato")
    
    doc["id"] = str(doc["_id"])
    
    # Enrich with product data from 'products' collection
    product_doc = db.products.find_one({"asin": doc["asin"]})
    if product_doc:
        # Calculate analysis
        analysis = analyze_product_price(product_doc)
        # Merge global product data with analysis
        doc["product"] = {**product_doc, "analysis": analysis}
        # Remove _id from nested product for serialization
        if "_id" in doc["product"]:
            del doc["product"]["_id"]
            
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
    asins = [doc.get("asin") for doc in articles if doc.get("asin")]
    products_cursor = db.products.find({"asin": {"$in": asins}}, {"asin": 1, "image_url": 1})
    products_map = {p["asin"]: p.get("image_url") for p in products_cursor}
    
    articles_list = []
    for doc in articles:
        doc["id"] = str(doc["_id"])
        # Use mapped image if available
        asin = doc.get("asin")
        if asin in products_map:
            doc["product_image_url"] = products_map[asin]
            
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
