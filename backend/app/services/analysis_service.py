from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def analyze_product_price(product):
    history = product.get("price_history", [])
    if not history or len(history) < 2:
        # Fallback for products with no history
        current_price = float(product.get("price", 0))
        return {
            "asin": product["asin"],
            "title": product["title"],
            "current_price": current_price,
            "min_price": current_price,
            "max_price": current_price,
            "avg_price": current_price,
            "recommendation": "HOLD",
            "reason": "Dati storici insufficienti per un'analisi approfondita. Monitora il prezzo per qualche giorno.",
            "trend": "stable",
            "risk_level": "Low",
            "volatility": 0.0,
            "is_favorite": product.get("is_favorite", False),
            "image_url": product.get("image_url"),
            "category": product.get("category", "N/A")
        }

    prices = [float(h["price"]) for h in history if h.get("price") is not None]
    if not prices:
        return None
        
    current_price = float(product.get("price", prices[-1]))
    
    min_price = min(prices)
    max_price = max(prices)
    avg_price = sum(prices) / len(prices)
    
    # If no variation yet (all prices same), we can't truly analyze
    if min_price == max_price:
        # Check how long we've been tracking
        try:
            first_date = datetime.fromisoformat(history[0]["date"].replace("Z", "+00:00"))
            tracking_duration = datetime.now() - first_date
            is_new = tracking_duration < timedelta(days=2)
        except:
            is_new = True

        reason = "Monitoraggio appena avviato. Non sono state ancora rilevate variazioni di prezzo per un'analisi accurata." if is_new else \
                 "Il prezzo è rimasto invariato negli ultimi giorni di monitoraggio. Ti consigliamo di attendere ancora o impostare un avviso."
        
        return {
            "asin": product["asin"],
            "title": product["title"],
            "current_price": current_price,
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price,
            "recommendation": "HOLD",
            "reason": reason,
            "trend": "stable",
            "risk_level": "Basso",
            "volatility": 0.0,
            "is_favorite": product.get("is_favorite", False),
            "image_url": product.get("image_url"),
            "category": product.get("category", "N/A"),
            "chance_of_drop": 50 if is_new else 40
        }

    # Trend calculation
    recent_prices = prices[-5:] if len(prices) >= 5 else prices
    trend = "stable"
    if len(recent_prices) >= 2:
        diff = recent_prices[-1] - recent_prices[0]
        if diff < -0.01:
            trend = "down"
        elif diff > 0.01:
            trend = "up"

    # Recommendation logic (AI Statistical Model)
    recommendation = "HOLD"
    reason = "Il prezzo è stabile e oscilla intorno alla media storica."
    
    # Probability of further drop (mock AI logic)
    chance_of_drop = 45 # Default lower risk if stable
    
    # Check if exact minimum
    if current_price <= min_price:
        recommendation = "BUY"
        reason = "🔥 Prezzo al minimo storico assoluto! È il momento perfetto per l'acquisto."
        chance_of_drop = 10
    # Check if very close to minimum (2% range)
    elif current_price <= min_price * 1.02:
        recommendation = "BUY"
        reason = "✅ Il prezzo è vicinissimo ai minimi storici. Ottima opportunità di risparmio."
        chance_of_drop = 20
    # Price is between min and average but trend is down
    elif current_price < avg_price and trend == "down":
        recommendation = "BUY"
        reason = "📉 Il prezzo sta calando ed è sotto la media. Un buon momento per approfittarne."
        chance_of_drop = 35
    # Price close to max and trend is up
    elif current_price >= max_price * 0.98 or (current_price > avg_price * 1.05 and trend == "up"):
        recommendation = "WAIT"
        reason = "⚠️ Prezzo in forte rialzo o vicino ai massimi. Consigliamo di attendere un rintracciamento."
        chance_of_drop = 75
    # Price significantly above average
    elif current_price > avg_price * 1.08:
        recommendation = "WAIT"
        reason = "⏳ Il prezzo attuale è superiore alla media storica. Meglio monitorare e attendere."
        chance_of_drop = 65
    # Price slightly below average (HOLD/Neutral)
    elif current_price < avg_price:
        recommendation = "HOLD"
        reason = "Prezzo leggermente sotto la media, ma non ancora ai livelli minimi. Puoi monitorare o acquistare se hai urgenza."
        chance_of_drop = 40
    else:
        recommendation = "HOLD"
        reason = "Il prezzo è leggermente sopra la media. Consigliamo di attendere un'offerta migliore."
        chance_of_drop = 55
        
    # Volatility / Risk
    volatility = (max_price - min_price) / avg_price if avg_price > 0 else 0
    risk_level = "Basso"
    if volatility > 0.4:
        risk_level = "Alto"
    elif volatility > 0.2:
        risk_level = "Medio"

    return {
        "asin": product["asin"],
        "title": product["title"],
        "current_price": current_price,
        "min_price": round(min_price, 2),
        "max_price": round(max_price, 2),
        "avg_price": round(avg_price, 2),
        "recommendation": recommendation,
        "reason": reason,
        "trend": trend,
        "risk_level": risk_level,
        "volatility": round(volatility * 100, 2),
        "is_favorite": product.get("is_favorite", False),
        "image_url": product.get("image_url"),
        "category": product.get("category", "N/A"),
        "chance_of_drop": chance_of_drop
    }

def get_market_analysis(products):
    if not products:
        return {
            "summary": {
                "total_tracked": 0,
                "buy_opportunities": 0,
                "wait_suggestions": 0,
                "at_all_time_low": 0,
                "market_sentiment": "Neutrale"
            },
            "items": []
        }
        
    analysis_results = [analyze_product_price(p) for p in products]
    analysis_results = [r for r in analysis_results if r]
    
    total_products = len(analysis_results)
    buy_count = len([r for r in analysis_results if r["recommendation"] == "BUY"])
    wait_count = len([r for r in analysis_results if r["recommendation"] == "WAIT"])
    hold_count = len([r for r in analysis_results if r["recommendation"] == "HOLD"])
    at_min_low = len([r for r in analysis_results if r["current_price"] <= r["min_price"]])
    
    # Sentiment calculation
    sentiment = "Neutrale"
    if buy_count > wait_count and buy_count > 0:
        sentiment = "Eccellente (Molte occasioni)"
    elif wait_count > buy_count:
        sentiment = "Attesa (Prezzi alti)"
    elif at_min_low > total_products / 3:
        sentiment = "Ottimo (Minimi storici rilevati)"
        
    return {
        "summary": {
            "total_tracked": total_products,
            "buy_opportunities": buy_count,
            "wait_suggestions": wait_count,
            "stable_items": hold_count,
            "at_all_time_low": at_min_low,
            "market_sentiment": sentiment,
            "avg_volatility": round(sum(r["volatility"] for r in analysis_results) / total_products, 2) if total_products > 0 else 0
        },
        "items": analysis_results
    }
