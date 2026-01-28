async def test_test_route(client):
    response = await client.get("/test/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert data["message"].startswith("it works!! :tada:")
    assert "users_count" in data
    assert isinstance(data["users_count"], int)
