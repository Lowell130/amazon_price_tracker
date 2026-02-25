from apscheduler.schedulers.background import BackgroundScheduler
from app.services.product_service import update_prices
from app.db import get_users_collection
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def update_all_products_job():
    logger.info("Starting automatic price update job...")
    try:
        users_collection = get_users_collection()
        # Update all products for all users
        update_prices(users_collection, user_filter=None)
        logger.info("Automatic price update job completed.")
    except Exception as e:
        logger.error(f"Error during automatic price update: {e}")

def start_scheduler():
    # Run every 12 hours. Removed immediate start to avoid scraping on every reload.
    scheduler.add_job(update_all_products_job, 'interval', hours=12)
    scheduler.start()
    logger.info("Scheduler started (interval: 12 hours). First run in 12 hours.")

def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("Scheduler shut down.")
