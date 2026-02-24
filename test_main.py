"""Tests for FastAPI application."""

import pytest
from httpx import AsyncClient
from main import app, get_default_cameras


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data


@pytest.mark.asyncio
async def test_get_cameras():
    """Test get all cameras endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/cameras")
        assert response.status_code == 200
        cameras = response.json()
        assert len(cameras) > 0
        assert cameras[0]["id"]
        assert cameras[0]["name"]
        assert cameras[0]["region"]
        assert cameras[0]["stream_url"]
        assert cameras[0]["poster_url"]


@pytest.mark.asyncio
async def test_get_cameras_by_region():
    """Test get cameras filtered by region."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/cameras?region=wc")
        assert response.status_code == 200
        cameras = response.json()
        assert len(cameras) > 0
        assert all(cam["region"] == "wc" for cam in cameras)


@pytest.mark.asyncio
async def test_get_camera_by_id():
    """Test get specific camera by ID."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/cameras/wc-lowers")
        assert response.status_code == 200
        camera = response.json()
        assert camera["id"] == "wc-lowers"
        assert camera["name"] == "Lowers"
        assert camera["region"] == "wc"


@pytest.mark.asyncio
async def test_get_camera_not_found():
    """Test get camera with invalid ID."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/cameras/nonexistent-camera")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_cameras_have_required_fields():
    """Test that all cameras have required fields."""
    cameras = get_default_cameras()
    for camera in cameras:
        assert camera.id
        assert camera.name
        assert camera.region
        assert camera.stream_url
        assert camera.poster_url


def test_camera_model_validation():
    """Test camera model validation."""
    from main import Camera
    
    camera = Camera(
        id="test-cam",
        name="Test Camera",
        region="test",
        stream_url="https://example.com/stream.m3u8",
        poster_url="https://example.com/poster.jpg"
    )
    assert camera.id == "test-cam"
    assert camera.name == "Test Camera"
    assert camera.region == "test"
