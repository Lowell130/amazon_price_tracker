import os
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Load environment variables from both root and backend directories
# Root .env
root_env = Path(os.getcwd()) / ".env"
if root_env.exists():
    load_dotenv(dotenv_path=root_env)

# Backend .env (can override root)
backend_env = BASE_DIR / ".env"
if backend_env.exists():
    load_dotenv(dotenv_path=backend_env, override=True)

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
BASE_URL = os.getenv("BASE_URL", "https://www.pricehub.it")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG", "default-tag")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# Telegram Configuration
TEL_TOKEN = os.getenv("TEL_TOKEN")
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "PriceTrackerBot")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# AI Content Generator
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGO_DB = os.getenv("MONGO_DB", "price_tracker")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


