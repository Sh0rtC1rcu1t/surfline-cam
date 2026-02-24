"""FastAPI application for Surfline camera streaming."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import os

app = FastAPI(
    title="Surfline Camera API",
    description="API for accessing Surfline camera data and streams",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Camera(BaseModel):
    """Camera data model."""
    id: str
    name: str
    region: str
    stream_url: str
    poster_url: str
    location: Optional[str] = None


class HealthCheck(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    version: str


def load_cameras() -> List[Camera]:
    """Load camera data from JSON file."""
    cameras_file = os.path.join(os.path.dirname(__file__), "data", "cameras.json")
    
    if not os.path.exists(cameras_file):
        return get_default_cameras()
    
    try:
        with open(cameras_file, "r") as f:
            data = json.load(f)
            return [Camera(**cam) for cam in data.get("cameras", [])]
    except (json.JSONDecodeError, ValueError):
        return get_default_cameras()


def get_default_cameras() -> List[Camera]:
    """Return default cameras for Southeastern NC."""
    return [
        Camera(
            id="ec-seabrooknh",
            name="Seabrook, NH",
            region="ec",
            stream_url="https://cams.cdn-surfline.com/cdn-ec/ec-seabrooknh/playlist.m3u8",
            poster_url="https://camstills.cdn-surfline.com/us-east-1/ec-seabrooknh/latest_small.jpg",
            location="Seabrook, New Hampshire"
        ),
        Camera(
            id="ec-hampton",
            name="Hampton Beach, NH",
            region="ec",
            stream_url="https://cams.cdn-surfline.com/cdn-ec/ec-hampton/playlist.m3u8",
            poster_url="https://camstills.cdn-surfline.com/us-east-1/ec-hampton/latest_small.jpg",
            location="Hampton Beach, New Hampshire"
        ),
        Camera(
            id="wc-lowers",
            name="Lowers",
            region="wc",
            stream_url="https://cams.cdn-surfline.com/cdn-wc/wc-lowers/playlist.m3u8",
            poster_url="https://camstills.cdn-surfline.com/us-west-2/wc-lowers/latest_small.jpg",
            location="San Clemente, California"
        ),
    ]


@app.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )


@app.get("/cameras", response_model=List[Camera])
async def get_cameras(region: Optional[str] = None) -> List[Camera]:
    """Get all cameras or filter by region."""
    cameras = load_cameras()
    
    if region:
        cameras = [cam for cam in cameras if cam.region == region]
    
    return cameras


@app.get("/cameras/{camera_id}", response_model=Camera)
async def get_camera(camera_id: str) -> Camera:
    """Get a specific camera by ID."""
    cameras = load_cameras()
    
    for cam in cameras:
        if cam.id == camera_id:
            return cam
    
    raise HTTPException(status_code=404, detail=f"Camera {camera_id} not found")


@app.get("/")
async def root():
    """Root endpoint with API documentation link."""
    return {
        "message": "Surfline Camera API",
        "docs": "/docs",
        "health": "/health",
        "cameras": "/cameras"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
