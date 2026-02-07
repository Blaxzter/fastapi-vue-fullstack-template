import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestHealthRoutes:
    async def test_healthz(self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    async def test_readyz(self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/readyz")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["database"] == "connected"
