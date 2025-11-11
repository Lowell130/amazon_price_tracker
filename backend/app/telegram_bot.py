import requests
from telegram import Bot
import asyncio
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
TEL_TOKEN = os.getenv("TEL_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


# Configurazione
# Configura il TOKEN del bot e l'ID chat
TELEGRAM_BOT_TOKEN = TEL_TOKEN
CHAT_ID = CHANNEL_ID
API_URL = "https://amazon-price-tracker-3kx4.onrender.com/api/public/price-drops"

async def get_price_drops():
    """Recupera i dati dall'API."""
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

async def resize_image(url, size=(300, 300)):
    """Ridimensiona l'immagine prima di inviarla a Telegram."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.thumbnail(size)  # Ridimensiona mantenendo le proporzioni
            img_with_padding = Image.new("RGB", size, (255, 255, 255))  # Aggiunge uno sfondo bianco
            img_with_padding.paste(img, ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2))
            output = BytesIO()
            img_with_padding.save(output, format="JPEG")
            output.seek(0)
            return output
    except Exception as e:
        print(f"Errore nel ridimensionamento immagine: {e}")
        return None

async def send_price_drops():
    """Invia i prodotti con calo di prezzo su Telegram"""
    drops = await get_price_drops()
    if not drops:
        print("❌ Nessun calo di prezzo trovato")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    for product in drops:  
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
                resized_image = await resize_image(image_url)
                if resized_image:
                    await bot.send_photo(chat_id=CHAT_ID, photo=resized_image, caption=message, parse_mode="Markdown")
                else:
                    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown", disable_web_page_preview=True)
            else:
                await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown", disable_web_page_preview=True)

            # ⏳ Aspetta 2 secondi prima di inviare il prossimo messaggio per evitare limiti di Telegram
            await asyncio.sleep(2)  

        except Exception as e:
            print("❌ Errore Telegram:", str(e))

if __name__ == "__main__":
    asyncio.run(send_price_drops())
