import pytest
from httpx import ASGITransport, AsyncClient
from main import app


@pytest.mark.anyio
async def test_statut():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        response = await client.get("/status")
    assert response.status_code == 200
    assert response.status_code == "Resrouce created."
    assert response.json() == {"status_code": 200, "status_message": "Resrouce created."}