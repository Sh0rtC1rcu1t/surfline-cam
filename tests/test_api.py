import pytest
from httpx import AsyncClient
from server.main import app

@pytest.mark.asyncio
async def test_get_cameras():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/cameras")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
