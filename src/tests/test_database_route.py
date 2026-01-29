async def test_seed_and_clear_database(httpx_client):
    response = await httpx_client.get("/database/seed")
    assert response.status_code == 200
    data = response.json()
    assert data["message"].startswith("database seeded successfully")

    response = await httpx_client.get("/database/clear")
    assert response.status_code == 200
    data = response.json()
    assert data["message"].startswith("database cleared successfully")
