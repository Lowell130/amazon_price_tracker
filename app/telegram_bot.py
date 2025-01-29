import requests
from telegram import Bot, InputMediaPhoto
import asyncio

# Configurazione
TELEGRAM_BOT_TOKEN = "7404452966:AAEQMpSGVlycpNLi5iv_AsBRLW0quTTwyMU"
CHAT_ID = "1078459133"
API_URL = "https://amazon-price-tracker-3kx4.onrender.com/api/public/price-drops"

async def get_price_drops():
    """Recupera i dati dall'API."""
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

async def send_price_drops():
    """Invia i prodotti con calo di prezzo su Telegram"""
    drops = await get_price_drops()
    if not drops:
        print("❌ Nessun calo di prezzo trovato")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    for product in drops[:5]:  # Invia massimo 5 prodotti per evitare spam
        title = product.get("title", "Sconosciuto")
        old_price = product.get("old_price", "N/A")
        new_price = product.get("new_price", "N/A")
        price_drop = product.get("price_drop", "N/A")
        category = product.get("category", "N/A")
        condition = product.get("condition", "N/A")
        rating = product.get("rating", "N/A")
        insertion_date = product.get("insertion_date", "N/A")
        image_url = product.get("image_url", None)  # URL immagine
        link = product.get("affiliate", "#")

        # Formatta il messaggio con Markdown
        message = (
            f"📉 *{title}*\n"
            f"🔻 *Calo:* -{price_drop}€\n"
            f"💰 *Prezzo vecchio:* {old_price} €\n"
            f"💲 *Prezzo nuovo:* {new_price} €\n"
            f"📌 *Categoria:* {category}\n"
            f"📦 *Condizione:* {condition}\n"
            f"⭐ *Rating:* {rating}/5\n"
            f"📅 *Data di inserimento:* {insertion_date}\n"
            f"🔗 [Acquista ora]({link})"
        )

        print("📩 Inviando messaggio Telegram:", message)  # 👀 Debug

        try:
            if image_url:
                await bot.send_photo(chat_id=CHAT_ID, photo=image_url, caption=message, parse_mode="Markdown")
            else:
                await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown", disable_web_page_preview=True)
        except Exception as e:
            print("❌ Errore Telegram:", str(e))

if __name__ == "__main__":
    asyncio.run(send_price_drops())
