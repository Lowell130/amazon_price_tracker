from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, products, admin, public, analysis, extension, articles, analytics, trends, seo, mascot
from app.db import users_collection
from app.config import BASE_URL
from datetime import datetime
import os
import logging
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
from app.scheduler import start_scheduler, shutdown_scheduler
from app.telegram_bot import start_bot, stop_bot

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    await start_bot()

@app.on_event("shutdown")
async def shutdown_event():
    shutdown_scheduler()
    await stop_bot()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "https://amazon-price-tracker-delta.vercel.app",
    "amazon-price-tracker-git-main-lowell130s-projects.vercel.app",
    "amazon-price-tracker-ndlrmkzir-lowell130s-projects.vercel.app",
    "https://pricehub.it",
    "https://www.pricehub.it",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://www.pricehub.it",
        "https://pricehub.it",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(admin.router)
app.include_router(public.router)
app.include_router(analysis.router)
app.include_router(extension.router)
app.include_router(articles.router)
app.include_router(analytics.router)
app.include_router(trends.router)
app.include_router(seo.router)
app.include_router(mascot.router)

@app.get("/")
async def root():
    return {"message": "Amazon Price Tracker API"}
