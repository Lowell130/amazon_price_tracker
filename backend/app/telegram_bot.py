import logging
import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from app.db import get_db, get_users_collection
from app.config import TEL_TOKEN

# Configurazione Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    logger.info("Telegram Bot avviato (async).")

async def stop_bot():
    """Ferma il bot Telegram."""
    global application
    if application:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        logger.info("Telegram Bot fermato.")
