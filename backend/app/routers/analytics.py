from fastapi import APIRouter, Depends, Query, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.db import get_db
from app.config import AFFILIATE_TAG
from datetime import datetime
from typing import Optional
from app.dependencies import admin_required

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

BOT_KEYWORDS = [
    "googlebot", "bingbot", "slurp", "duckduckbot", "baiduspider", "yandexbot",
    "sogou", "exabot", "facebot", "ia_archiver", "headlesschrome", "crawler",
    "spider", "robot", "bot/", "bot "
]

def is_bot_user_agent(ua: str) -> bool:
    if not ua:
        return False
    ua_lower = ua.lower()
    return any(keyword in ua_lower for keyword in BOT_KEYWORDS)

@router.post("/visit")
async def record_visit(request: Request):
    """Records a site visit with referrer, path, search query and bot detection."""
    data = await request.json()
    db = get_db()
    
    user_agent = request.headers.get("user-agent", "")
    is_bot = is_bot_user_agent(user_agent)
    
    visit_doc = {
        "type": "visit",
        "referrer": data.get("referrer", "direct"),
        "path": data.get("path", "/"),
        "utm_source": data.get("utm_source"),
        "utm_medium": data.get("utm_medium"),
        "utm_campaign": data.get("utm_campaign"),
        "search_query": data.get("search_query"),
        "user_agent": user_agent,
        "is_bot": is_bot,
        "timestamp": datetime.utcnow()
    }
    
    # Non salviamo le visite dei BOT per non saturare lo spazio del DB
    if not is_bot:
        db.analytics.insert_one(visit_doc)
        
    return {"status": "ok", "is_bot": is_bot}

@router.get("/r/{asin}")
async def affiliate_redirect(request: Request, asin: str, ref: Optional[str] = Query(None)):
    """Logs an affiliate click and redirects to Amazon, blocking bots."""
    db = get_db()
    
    user_agent = request.headers.get("user-agent", "")
    is_bot = is_bot_user_agent(user_agent)
    
    click_doc = {
        "type": "click",
        "asin": asin,
        "referrer_on_click": ref,
        "user_agent": user_agent,
        "is_bot": is_bot,
        "timestamp": datetime.utcnow()
    }
    
    if is_bot:
        raise HTTPException(status_code=403, detail="Bot traffic is not permitted for affiliate redirects")
        
    # Salviamo solo se non è un bot
    db.analytics.insert_one(click_doc)
    
    # Construct Amazon link with affiliate tag
    amazon_url = f"https://www.amazon.it/gp/product/{asin}/?tag={AFFILIATE_TAG}"
    return RedirectResponse(url=amazon_url, status_code=302)

@router.get("/admin/stats")
async def get_analytics_stats(
    include_bots: bool = Query(False),
    admin: dict = Depends(admin_required)
):
    """Returns aggregated stats for the admin dashboard, optionally including bots."""
    db = get_db()
    
    # Filter for visits
    visit_filter = {"type": "visit"}
    if not include_bots:
        visit_filter["is_bot"] = {"$ne": True}
        
    # 1. Total Visits
    total_visits = db.analytics.count_documents(visit_filter)
    
    # 2. Total Clicks
    click_filter = {"type": "click"}
    if not include_bots:
        click_filter["is_bot"] = {"$ne": True}
        
    total_clicks = db.analytics.count_documents(click_filter)
    
    # 3. Top Referrers (Visits) with details
    pipeline_referrers = [
        {"$match": visit_filter},
        {
            "$group": {
                "_id": "$referrer",
                "count": {"$sum": 1},
                "bot_count": {"$sum": {"$cond": [{"$eq": ["$is_bot", True]}, 1, 0]}},
                "queries": {"$addToSet": "$search_query"},
                "top_path": {"$first": "$path"}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_referrers = list(db.analytics.aggregate(pipeline_referrers))
    
    formatted_referrers = []
    for r in top_referrers:
        queries = [q for q in r.get("queries", []) if q]
        formatted_referrers.append({
            "source": r["_id"],
            "count": r["count"],
            "bot_count": r.get("bot_count", 0),
            "is_mostly_bot": r.get("bot_count", 0) > (r["count"] / 2),
            "top_query": queries[0] if queries else None,
            "top_path": r.get("top_path")
        })
    
    # 4. Top Search Queries
    query_filter = {**visit_filter, "search_query": {"$ne": None, "$ne": ""}}
    pipeline_queries = [
        {"$match": query_filter},
        {"$group": {"_id": "$search_query", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_queries = list(db.analytics.aggregate(pipeline_queries))

    # 5. Top Paths (to see popular pages or bot probes)
    pipeline_paths = [
        {"$match": visit_filter},
        {"$group": {"_id": "$path", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_paths = list(db.analytics.aggregate(pipeline_paths))
    
    # 6. Top Clicked Products
    pipeline_products = [
        {"$match": click_filter},
        {"$group": {"_id": "$asin", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_products = list(db.analytics.aggregate(pipeline_products))
    
    # Enrich top products
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
            "ctr": round((total_clicks / total_visits * 100), 2) if total_visits > 0 else 0,
            "include_bots": include_bots
        },
        "top_referrers": formatted_referrers,
        "top_queries": [{"query": q["_id"], "count": q["count"]} for q in top_queries],
        "top_paths": [{"path": p["_id"], "count": p["count"]} for p in top_paths],
        "top_products": enriched_products
    }

@router.delete("/admin/clear")
async def clear_analytics_data(admin: dict = Depends(admin_required)):
    """Deletes all analytics data (visits and clicks)."""
    print(f"DEBUG: Clearing analytics data by admin {admin.get('username')}")
    db = get_db()
    db.analytics.delete_many({})
    return {"message": "Dati analytics cancellati con successo."}
