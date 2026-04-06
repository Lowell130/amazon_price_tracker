import feedparser
import json
import logging
import hashlib
import requests
from google import genai
from datetime import datetime, timedelta
from app.config import GEMINI_API_KEY
from app.db import get_db, get_settings_collection

logger = logging.getLogger(__name__)

# CURRENT VERSION for default feeds. If incremented, the system will re-merge missing defaults once.
CURRENT_RSS_VERSION = 2

# Fallback basic list if DB has no setup
DEFAULT_RSS_FEEDS = [
    # Top Tech News
    "https://www.theverge.com/tech/rss/index.xml",
    "https://www.hwupgrade.it/rss_news.xml",
    "https://www.webnews.it/feed/",
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/category/gear/latest/rss",
    "https://www.engadget.com/rss.xml",
    # Social Signals (Reddit / HN)
    "https://www.reddit.com/r/technology/top/.rss?t=day",
    "https://www.reddit.com/r/gadgets/top/.rss?t=day",
    "https://news.ycombinator.com/rss",
    # Google Trends IT (Corrected URL)
    "https://trends.google.it/trends/trendingsearches/daily/rss?geo=IT",
    # YouTube Tech Influencers (RSS via Channel ID)
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCBJycsmduvYEL83R_U4JriQ", # MKBHD
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC_MneQC6777Zag6I6L_u88A"  # MrWhoseTheBoss
]

def get_rss_sources() -> list:
    """Reads RSS sources from DB and merges new defaults ONLY if version increases."""
    settings = get_settings_collection()
    doc = settings.find_one({"type": "rss_sources"})
    
    if not doc:
        settings.insert_one({
            "type": "rss_sources", 
            "urls": DEFAULT_RSS_FEEDS,
            "version": CURRENT_RSS_VERSION
        })
        return DEFAULT_RSS_FEEDS
    
    current_urls = doc.get("urls", [])
    db_version = doc.get("version", 0)
    
    # Only merge missing defaults if the database code version is older than CURRENT_RSS_VERSION
    if db_version < CURRENT_RSS_VERSION:
        added = False
        for url in DEFAULT_RSS_FEEDS:
            if url not in current_urls:
                current_urls.append(url)
                added = True
        
        # Update both URL list and Version so this block only runs once per increment
        settings.update_one(
            {"type": "rss_sources"}, 
            {"$set": {"urls": current_urls, "version": CURRENT_RSS_VERSION}}
        )
        
    return current_urls

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
    """Fetches the latest headlines using requests (with User-Agent) + feedparser."""
    news_items = []
    
    # Common User-Agent to avoid getting blocked by Reddit/Social sources
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for url in get_rss_sources():
        try:
            logger.info(f"Fetching RSS: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Skipping RSS {url}: Status {response.status_code}")
                continue
                
            # Parse the XML content from requests
            feed = feedparser.parse(response.content)
            
            # Pick top 20 entries from each feed (increased for broader view)
            for entry in feed.entries[:20]:
                title = entry.get("title", "")
                # Some feeds use 'description' if 'summary' is missing, or vice versa
                summary = entry.get("summary") or entry.get("description") or ""
                
                if title:
                    # Clean up long descriptions to avoid context bloat
                    clean_summary = summary[:300] if summary else "No description"
                    news_items.append(f"Source: {url} | Title: {title} | Description: {clean_summary}")
        except Exception as e:
            logger.error(f"Error fetching RSS {url}: {e}")
            
    return "\n".join(news_items)

async def scan_and_analyze_trends(target_count: int = 10):
    """Fetches news and asks Gemini to extract market trends, with MongoDB caching."""
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not configured. Cannot generate trends.")
        return []

    logger.info("Fetching latest RSS feeds for trend analysis...")
    news_text = fetch_latest_news()
    
    if not news_text:
        return []

    # --- Cache Logic ---
    # Create a unique hash of the current news content and requested count
    content_hash = hashlib.sha256(f"{news_text}_{target_count}".encode()).hexdigest()
    db = get_db()
    
    # Check if we have a recent cached result for this exact content
    # We allow a cache hit if the hash matches and it's less than 12 hours old
    cache_expiry = datetime.utcnow() - timedelta(hours=12)
    cached_result = db.ai_cache.find_one({
        "hash": content_hash,
        "type": "trends",
        "timestamp": {"$gt": cache_expiry}
    })
    
    if cached_result:
        logger.info("Cache HIT: Returning previously analyzed trends for this content.")
        return cached_result.get("trends", [])

    # --- End Cache Logic ---

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    Act as a senior tech market analyst and SEO expert. 
    I will provide you with a high-density stream of headlines and snippets from major tech news sites, social media (Reddit), and search trends.
    Read them carefully and identify exactly {target_count} specific products, product categories, or tech trends that are currently gaining traction.
    
    CRITICAL INSTRUCTION FOR DIVERSITY: 
    Do NOT focus only on the 1-2 biggest news of the day (e.g. if everyone is talking about a new iPhone, only give me 1 trend about it). 
    I want a broad view across different niches. Distributed the {target_count} trends across these categories where possible:
    - Gaming (Hardware/Peripherals)
    - Smart Home / IoT
    - PC Components / Computing
    - Wearables / Audio
    - Smartphones / Mobile Tech
    - Home Office / Productivity
    - Emerging Tech (AI Gadgets, VR/AR)

    Focus ONLY on actionable consumer electronics or gadgets that people might buy on Amazon.
    If you see a niche but rising product, prioritize it over a mainstream but over-covered topic.

    for each trend, output:
    1. "topic": the name of the product or category (e.g. "Monitor OLED 240Hz", "Meta Quest 3")
    2. "seo_keyword": a high-converting, click-worthy long-tail SEO keyword to write an article about (e.g. "I 5 Migliori Monitor OLED 240Hz del 2026")
    3. "score": a virality score from 1 to 100 based on the news impact
    4. "reason": a short 1-sentence motivation explaining why it's trending based on the news you read.
    5. "sentiment": one of ["Hot 🔥", "Positive ✨", "Controversial 🧐", "Neutral ⚖️"]
    6. "profitability": a dynamic score from 1 to 100 based on the ACTUAL intent to purchase products related to this trend on Amazon.
    7. "suggested_products": a list of 2-3 specific product names or terms to search on Amazon (e.g. ["LG UltraGear OLED", "Samsung Odyssey G9"])
    
    News data to analyze:
    {news_text}
    
    Format the response strictly as valid JSON observing this format:
    {{
        "trends": [
            {{
                "topic": "...",
                "seo_keyword": "...",
                "score": 90,
                "reason": "...",
                "sentiment": "...",
                "profitability": 0, // MUST be a dynamic, calculated score (do not always use the same number)
                "suggested_products": ["...", "..."]
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
        
        # Save to Cache for efficiency
        db.ai_cache.update_one(
            {"hash": content_hash, "type": "trends"},
            {
                "$set": {
                    "timestamp": datetime.utcnow(),
                    "trends": trends
                }
            },
            upsert=True
        )

        # Save to DB for history
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
