from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import RedirectResponse
from app.db import get_db
from app.config import AFFILIATE_TAG
from datetime import datetime
from typing import Optional
from app.dependencies import admin_required

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.post("/visit")
async def record_visit(request: Request):
    """Records a site visit with referrer and path."""
    data = await request.json()
    db = get_db()
    
    visit_doc = {
        "type": "visit",
        "referrer": data.get("referrer", "direct"),
        "path": data.get("path", "/"),
        "utm_source": data.get("utm_source"),
        "utm_medium": data.get("utm_medium"),
        "utm_campaign": data.get("utm_campaign"),
        "user_agent": request.headers.get("user-agent"),
        "timestamp": datetime.utcnow()
    }
    
    db.analytics.insert_one(visit_doc)
    return {"status": "ok"}

@router.get("/r/{asin}")
async def affiliate_redirect(asin: str, ref: Optional[str] = Query(None)):
    """Logs an affiliate click and redirects to Amazon."""
    db = get_db()
    
    click_doc = {
        "type": "click",
        "asin": asin,
        "referrer_on_click": ref,
        "timestamp": datetime.utcnow()
    }
    
    db.analytics.insert_one(click_doc)
    
    # Construct Amazon link with affiliate tag
    amazon_url = f"https://www.amazon.it/gp/product/{asin}/?tag={AFFILIATE_TAG}"
    return RedirectResponse(url=amazon_url, status_code=302)

@router.get("/admin/stats")
async def get_analytics_stats(admin: dict = Depends(admin_required)):
    """Returns aggregated stats for the admin dashboard."""
    db = get_db()
    
    # 1. Total Visits
    total_visits = db.analytics.count_documents({"type": "visit"})
    
    # 2. Total Clicks
    total_clicks = db.analytics.count_documents({"type": "click"})
    
    # 3. Top Referrers (Visits)
    pipeline_referrers = [
        {"$match": {"type": "visit"}},
        {"$group": {"_id": "$referrer", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_referrers = list(db.analytics.aggregate(pipeline_referrers))
    
    # 4. Top Clicked Products
    pipeline_products = [
        {"$match": {"type": "click"}},
        {"$group": {"_id": "$asin", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_products = list(db.analytics.aggregate(pipeline_products))
    
    # Enrich top products with titles if available
    enriched_products = []
    for p in top_products:
        prod_info = db.products.find_one({"asin": p["_id"]}, {"title": 1, "image_url": 1})
        if prod_info:
            enriched_products.append({
                "asin": p["_id"],
                "count": p["count"],
                "title": prod_info.get("title", "Sconosciuto"),
                "image_url": prod_info.get("image_url")
            })
        else:
            enriched_products.append({
                "asin": p["_id"],
                "count": p["count"],
                "title": f"Prodotto {p['_id']}",
                "image_url": None
            })

    return {
        "summary": {
            "total_visits": total_visits,
            "total_clicks": total_clicks,
            "ctr": round((total_clicks / total_visits * 100), 2) if total_visits > 0 else 0
        },
        "top_referrers": [{"source": r["_id"], "count": r["count"]} for r in top_referrers],
        "top_products": enriched_products
    }

@router.delete("/admin/clear")
async def clear_analytics_data(admin: dict = Depends(admin_required)):
    """Deletes all analytics data (visits and clicks)."""
    print(f"DEBUG: Clearing analytics data by admin {admin.get('username')}")
    db = get_db()
    db.analytics.delete_many({})
    return {"message": "Dati analytics cancellati con successo."}
