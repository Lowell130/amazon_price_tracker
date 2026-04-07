from fastapi import APIRouter, Depends, Query
from app.db import get_db
from app.dependencies import admin_required
from app.services.mascot_service import generate_mascot_chat_response, update_mascot_xp, generate_passive_mascot_thought
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import random

router = APIRouter(prefix="/api/mascot", tags=["mascot"])

class ChatRequest(BaseModel):
    message: str

def get_mascot_data():
    db = get_db()
    mascot = db.mascot.find_one({"type": "kitten"})
    if not mascot:
        mascot = {
            "type": "kitten",
            "name": "Pricey",
            "level": 1,
            "xp": 0,
            "next_level_xp": 100,
            "mood": "happy",
            "last_interaction": datetime.utcnow()
        }
        db.mascot.insert_one(mascot)
    return mascot

@router.get("")
async def get_mascot_state(admin: dict = Depends(admin_required)):
    """Returns the current state of Pricey the AI Kitten."""
    db = get_db()
    mascot = get_mascot_data()
    
    # Calculate mood based on recent stats
    # 1. Traffic (visits in last 24h)
    from datetime import timedelta
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_visits = db.analytics.count_documents({"type": "visit", "timestamp": {"$gt": yesterday}})
    
    # 2. Performance (clicks in last 24h)
    recent_clicks = db.analytics.count_documents({"type": "click", "timestamp": {"$gt": yesterday}})
    
    # 3. Price Drops
    # (Just a mock check for now, can be sophisticated later)
    
    mood = "happy"
    if recent_visits > 50:
        mood = "energetic"
    elif recent_clicks > 10:
        mood = "excited"
    elif recent_visits < 5:
        mood = "sleepy"
        
    # 3. Dynamic Thought (AI with 1h Cache)
    passive_msg = mascot.get("passive_message")
    expires = mascot.get("passive_message_expires")
    
    if not passive_msg or not expires or datetime.utcnow() > expires:
        # Generate new thought
        passive_msg = await generate_passive_mascot_thought()
        # Set expiry to 1 hour from now
        expires = datetime.utcnow() + timedelta(hours=1)
        
        db.mascot.update_one(
            {"type": "kitten"},
            {"$set": {
                "passive_message": passive_msg,
                "passive_message_expires": expires
            }}
        )
        
    return {
        "name": mascot["name"],
        "level": mascot["level"],
        "xp": mascot["xp"],
        "next_level_xp": mascot["next_level_xp"],
        "mood": mood,
        "message": passive_msg,
        "last_scrape_data": mascot.get("last_scrape_data")
    }

@router.post("/interact")
async def interact(action: str = Query(...), admin: dict = Depends(admin_required)):
    """Handles interactions like petting or feeding."""
    db = get_db()
    mascot = get_mascot_data()
    
    xp_gain = 0
    if action == "pet":
        xp_gain = 5
    elif action == "feed":
        xp_gain = 10
        
    new_xp = mascot["xp"] + xp_gain
    new_level = mascot["level"]
    next_level_xp = mascot["next_level_xp"]
    
    if new_xp >= next_level_xp:
        new_level += 1
        new_xp -= next_level_xp
        next_level_xp = int(next_level_xp * 1.5)
        
    db.mascot.update_one(
        {"type": "kitten"},
        {"$set": {
            "xp": new_xp,
            "level": new_level,
            "next_level_xp": next_level_xp,
            "last_interaction": datetime.utcnow()
        }}
    )
    
    return {"status": "ok", "xp_gained": xp_gain, "new_level": new_level > mascot["level"]}

@router.post("/chat")
async def chat_with_mascot(
    request: ChatRequest,
    admin: dict = Depends(admin_required)
):
    """Conversational AI endpoint for Pricey the kitten."""
    response = await generate_mascot_chat_response(request.message)
    
    # Award small XP for socializing
    update_mascot_xp(2)
    
    return {"response": response}

def generate_kitten_message(mood: str, stats: dict) -> str:
    """Fallback generator for kitten messages. 
    In a full implementation, this could call an LLM.
    """
    messages = {
        "happy": [
            "Miao! Tutto sembra calmo e sotto controllo oggi.",
            "Fare le fusa è il mio hobby preferito, quasi quanto tracciare prezzi!",
            "Hai visto quanti prodotti stiamo monitorando? Siamo fortissimi!"
        ],
        "energetic": [
            "Wow! C'è un sacco di movimento sul sito oggi! Miao!",
            "Sento l'energia dei visitatori! Corriamo a vedere le offerte!",
            "Il traffico sta salendo, prepariamoci a nuovi clic!"
        ],
        "excited": [
            "Qualcuno ha detto SCONTI? Ho visto dei cali di prezzo pazzeschi!",
            "Miao miao! I clic volano oggi! Stiamo andando alla grande!",
            "È il momento perfetto per pubblicare un nuovo articolo!"
        ],
        "sleepy": [
            "Ronf... il sito è un po' silenzioso oggi. Forse è ora di aggiungere qualche prodotto?",
            "Miao... mi sento un po' pigro. Portami qualche nuovo visitatore!",
            "Un gattino ha bisogno di azione! Dove sono finiti tutti?"
        ]
    }
    
    options = messages.get(mood, messages["happy"])
    return random.choice(options)
