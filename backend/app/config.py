import os
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
# If .env not in backend, check root
if not env_path.exists():
    env_path = BASE_DIR.parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
BASE_URL = os.getenv("BASE_URL", "https://www.pricehub.it")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG", "default-tag")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Telegram Configuration
TEL_TOKEN = os.getenv("TEL_TOKEN")
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "PriceTrackerBot")
CHANNEL_ID = os.getenv("CHANNEL_ID")


