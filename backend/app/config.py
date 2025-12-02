import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
BASE_URL = os.getenv("BASE_URL", "https://www.pricehub.it")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG", "default-tag")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


