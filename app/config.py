# app/config.py
from amazon_paapi import AmazonApi
SECRET_KEY = "your_secret_key"  # Cambiare questa chiave con una chiave sicura
ACCESS_KEY = "AKIAJ26QQSH5D3LZGHGQ"
SECRET_KEY = "yehnwB7alUyy4lsh9UxrmrDEITXZ5qEzrChfVReT"
PARTNER_TAG = "newdev-21"
REGION = "IT"  # Regione Amazon
amazon_api = AmazonApi(ACCESS_KEY, SECRET_KEY, PARTNER_TAG, REGION)
