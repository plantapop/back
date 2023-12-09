import pytest


@pytest.mark.acceptance
async def test_readiness(client):
    response = await client.get("/readiness")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
