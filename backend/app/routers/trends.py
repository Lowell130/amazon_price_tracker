from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel
from typing import List, Dict, Any
from app.dependencies import admin_required
from app.services.trend_service import get_latest_trends, scan_and_analyze_trends, get_rss_sources, add_rss_source, remove_rss_source

router = APIRouter(prefix="/api/admin/trends", tags=["trends"])

class RefreshTrendsRequest(BaseModel):
    count: int = 10

class RssSourceRequest(BaseModel):
    url: str

@router.get("", response_model=List[Dict[str, Any]])
async def get_trends(admin: dict = Depends(admin_required)):
    """Returns the latest analyzed trend signals from MongoDB."""
    trends = get_latest_trends()
    return trends

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def force_refresh_trends(data: RefreshTrendsRequest, admin: dict = Depends(admin_required)):
    """Forces an immediate RSS scan and AI trend extraction with requested count."""
    trends = await scan_and_analyze_trends(target_count=data.count)
    if not trends:
        raise HTTPException(status_code=500, detail="Failed to analyze trends. Check logs or Gemini constraints.")
    return {"status": "success", "trends": trends}

@router.get("/sources", response_model=List[str])
async def get_sources_api(admin: dict = Depends(admin_required)):
    return get_rss_sources()

@router.post("/sources", status_code=201)
async def add_source_api(data: RssSourceRequest, admin: dict = Depends(admin_required)):
    add_rss_source(data.url)
    return {"status": "success", "urls": get_rss_sources()}

@router.delete("/sources", status_code=200)
async def remove_source_api(data: RssSourceRequest, admin: dict = Depends(admin_required)):
    remove_rss_source(data.url)
    return {"status": "success", "urls": get_rss_sources()}
