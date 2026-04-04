import feedparser
import json
import logging
from google import genai
from datetime import datetime
from app.config import GEMINI_API_KEY
from app.db import get_db, get_settings_collection

logger = logging.getLogger(__name__)

# Fallback basic list if DB has no setup
DEFAULT_RSS_FEEDS = [
    "https://www.theverge.com/tech/rss/index.xml",
    "https://www.hwupgrade.it/rss_news.xml",
    "https://www.tomshw.it/feed",
    "https://techcrunch.com/feed/"
]

def get_rss_sources() -> list:
    """Reads RSS sources from DB or initializes with defaults."""
    settings = get_settings_collection()
    doc = settings.find_one({"type": "rss_sources"})
    if not doc or not doc.get("urls"):
        return DEFAULT_RSS_FEEDS
    return doc["urls"]

def add_rss_source(url: str):
    settings = get_settings_collection()
    doc = settings.find_one({"type": "rss_sources"})
    if not doc:
        settings.insert_one({"type": "rss_sources", "urls": DEFAULT_RSS_FEEDS + [url]})
    else:
        urls = doc.get("urls", [])
        if url not in urls:
            settings.update_one({"type": "rss_sources"}, {"$push": {"urls": url}})

def remove_rss_source(url: str):
    settings = get_settings_collection()
    settings.update_one({"type": "rss_sources"}, {"$pull": {"urls": url}})

def fetch_latest_news() -> str:
    """Fetches the latest headlines from predefined RSS feeds."""
    news_items = []
    
    for url in get_rss_sources():
        try:
            feed = feedparser.parse(url)
            # Pick top 10 entries from each feed to not overload context but still provide depth
            for entry in feed.entries[:10]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                # Clean up summary slightly (e.g. basic HTML tags removal could be done, but Gemini parses HTML fine)
                if title:
                    news_items.append(f"Title: {title} | Description: {summary[:200]}")
        except Exception as e:
            logger.error(f"Error fetching RSS {url}: {e}")
            
    return "\n".join(news_items)

async def scan_and_analyze_trends(target_count: int = 10):
    """Fetches news and asks Gemini to extract market trends, returning the structured data."""
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not configured. Cannot generate trends.")
        return []

    logger.info("Fetching latest RSS feeds for trend analysis...")
    news_text = fetch_latest_news()
    
    if not news_text:
        return []

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    Act as a senior tech market analyst and SEO expert.
    I will provide you with the latest headlines and snippets from major technology news websites.
    Read them carefully and identify exactly {target_count} specific products, product categories, or tech trends that are currently gaining huge traction, hype, or are widely featured today.
    
    Focus ONLY on actionable consumer electronics, PC hardware, smart home, or gadgets that people might buy on Amazon.
    
    For each trend, output:
    1. "topic": the name of the product or category (e.g. "Monitor OLED 240Hz", "Meta Quest 3")
    2. "seo_keyword": a high-converting, click-worthy long-tail SEO keyword to write an article about (e.g. "I 5 Migliori Monitor OLED 240Hz del 2026")
    3. "score": a virality score from 1 to 100 based on the news impact
    4. "reason": a short 1-sentence motivation explaining why it's trending based on the news you read.
    
    News data to analyze:
    {news_text}
    
    Format the response strictly as valid JSON observing this format:
    {{
        "trends": [
            {{
                "topic": "...",
                "seo_keyword": "...",
                "score": 90,
                "reason": "..."
            }}
        ]
    }}
    """
    
    try:
        logger.info("Sending news to Gemini for trend analysis...")
        config = genai.types.GenerateContentConfig(
            response_mime_type="application/json"
        )
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt,
            config=config
        )
        data = json.loads(response.text.strip())
        trends = data.get("trends", [])
        
        # Save to DB for history/storage
        db = get_db()
        doc = {
            "timestamp": datetime.utcnow(),
            "trends": trends
        }
        db.trends_history.insert_one(doc)
        
        return trends
    except Exception as e:
        logger.error(f"Error analyzing trends: {e}")
        return []

def get_latest_trends():
    """Retrieves the most recent trend analysis from the internal DB."""
    db = get_db()
    latest = db.trends_history.find_one({}, sort=[("timestamp", -1)])
    if latest:
        # Convert ObjectId
        latest["_id"] = str(latest["_id"])
        return latest.get("trends", [])
    return []
