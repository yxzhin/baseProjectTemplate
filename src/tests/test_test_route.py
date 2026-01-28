async def test_test_route(httpx_client):
    """
    Тестирует маршрут /test/ API сервера.
    Проверяет, что ответ содержит ожидаемые поля и значения.
    """
    response = await httpx_client.get("/test/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert data["message"].startswith("it works!! :tada:")
    assert "users_count" in data
    assert isinstance(data["users_count"], int)
