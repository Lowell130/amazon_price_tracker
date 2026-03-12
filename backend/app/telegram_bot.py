import logging
import asyncio
import os
from telegram import Update
from telegram.error import Conflict, NetworkError
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from app.db import get_db, get_users_collection
from app.config import TEL_TOKEN, CHANNEL_ID
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Silenzia i log interni di telegram per evitare il rumore durante il reload
logging.getLogger("telegram.ext.Updater").setLevel(logging.CRITICAL)
logging.getLogger("telegram.ext._updater").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Global application instance
application = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestisce il comando /start con o senza token."""
    chat_id = update.effective_chat.id
    args = context.args

    if not args:
        await context.bot.send_message(
            chat_id=chat_id, 
            text="Ciao! Per collegare il tuo account, usa il link generato dal sito web."
        )
        return

    token = args[0]
    db = get_db()
    users_collection = get_users_collection()

    # Cerca il token nel DB
    token_doc = db.telegram_tokens.find_one({"token": token})

    if not token_doc:
        await context.bot.send_message(
            chat_id=chat_id, 
            text="Token non valido o scaduto. Genera un nuovo link dal sito."
        )
        return

    # Token trovato: collega l'utente
    username = token_doc["username"]
    
    # Aggiorna l'utente con il chat_id
    result = users_collection.update_one(
        {"username": username},
        {"$set": {"telegram_chat_id": str(chat_id)}}
    )

    if result.modified_count > 0:
        # Rimuovi il token usato
        db.telegram_tokens.delete_one({"_id": token_doc["_id"]})
        
        await context.bot.send_message(
            chat_id=chat_id, 
            text=f"Account collegato con successo! Ciao {username}, riceverai qui le notifiche sui cali di prezzo."
        )
        logger.info(f"User {username} linked to chat_id {chat_id}")
    else:
        await context.bot.send_message(
            chat_id=chat_id, 
            text="Errore nel collegamento dell'account. Riprova."
        )

async def start_bot():
    """Avvia il bot Telegram come task di background."""
    global application
    if not TEL_TOKEN:
        logger.error("TEL_TOKEN non trovato. Il bot non verrà avviato.")
        return

    application = ApplicationBuilder().token(TEL_TOKEN).build()
    
    # Gestore errori globale per silenziare i conflitti attesi
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        if isinstance(context.error, Conflict):
            logger.debug("Telegram Conflict ignorato nel gestore errori.")
            return
        logger.error("Eccezione non gestita nel bot Telegram:", exc_info=context.error)

    application.add_error_handler(error_handler)
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    await application.initialize()
    await application.start()
    
    try:
        await application.updater.start_polling(drop_pending_updates=True)
        logger.info("Telegram Bot avviato (polling attivo).")
    except Conflict:
        logger.warning("Conflitto Telegram Bot rilevato (probabile reload in corso). La nuova istanza prenderà il controllo a breve.")
    except Exception as e:
        logger.error(f"Errore durante l'avvio del polling Telegram: {e}")

async def stop_bot():
    """Ferma il bot Telegram."""
    global application
    if application:
        try:
            if application.updater and application.updater.running:
                await application.updater.stop()
            await application.stop()
            await application.shutdown()
            logger.info("Telegram Bot fermato correttamente.")
        except Exception as e:
            logger.error(f"Errore durante lo stop del bot Telegram: {e}")
        finally:
            application = None

def broadcast_price_drops():
    """Legge l'ultimo report e lo invia al canale Telegram."""
    if not TEL_TOKEN or not CHANNEL_ID:
        logger.error("Configurazione Telegram incompleta (Token o Channel ID mancanti).")
        return

    db = get_db()
    price_drops_collection = db["price_drops"]
    report = price_drops_collection.find_one(sort=[("generation_date", -1)])

    if not report or not report.get("drops"):
        logger.info("Nessun calo di prezzo da inviare.")
        return

    logger.info(f"Invio di {len(report['drops'])} cali di prezzo al canale {CHANNEL_ID}...")

    for drop in report["drops"]:
        message = (
            f"📉 *{drop.get('title', 'Prodotto')}*\n"
            f"🔻 *Prezzo:* {drop['new_price']}€ (era {drop['old_price']}€)\n"
            f"💰 *Risparmio:* {drop['price_drop']}€\n"
            f"🔗 [Vedi su Amazon]({drop.get('affiliate') or 'https://www.amazon.it/gp/product/' + drop['asin']})"
        )
        
        try:
            requests.post(
                f"https://api.telegram.org/bot{TEL_TOKEN}/sendMessage",
                data={
                    "chat_id": CHANNEL_ID,
                    "text": message,
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": False
                },
                timeout=10
            )
            time.sleep(1) # Evita limiti di velocità
        except Exception as e:
            logger.error(f"Errore nell'invio del drop {drop['asin']}: {e}")

    logger.info("Broadcast completato.")

if __name__ == "__main__":
    import time
    broadcast_price_drops()
