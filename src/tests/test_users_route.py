async def test_add_and_get_user_by_id(client, create_user):
    user = await create_user(73733737, "ril73_test37")

    response = await client.get(f"/users/{user['discord_id']}")
    assert response.status_code == 200

    fetched = response.json()
    assert fetched["id"] == user["id"]
    assert fetched["discord_id"] == user["discord_id"]
    assert fetched["username"] == user["username"]
    assert fetched["avatar_url"] == user["avatar_url"]


async def test_add_and_get_user_by_username(client, create_user):
    user = await create_user(37377373, "ril37_test73")

    response = await client.get(f"/users/username/{user['username']}")
    assert response.status_code == 200

    fetched = response.json()
    assert fetched["id"] == user["id"]
    assert fetched["discord_id"] == user["discord_id"]
    assert fetched["username"] == user["username"]
    assert fetched["avatar_url"] == user["avatar_url"]


async def test_get_users(client, create_user):
    users = []
    for i in range(15):
        user = await create_user(7373 + i + 37, f"test_user_{i}")
        users.append(user)

    # test default pagination (page=1, limit=10)
    response = await client.get("/users/")
    assert response.status_code == 200

    fetched = response.json()
    fetched_users = fetched["users"]
    total = fetched["total"]

    assert total == 10
    assert fetched_users[0]["id"] == users[0]["id"]
    assert fetched_users[9]["id"] == users[9]["id"]

    # test page=2, limit=5
    response = await client.get("/users/?page=2&limit=5")
    assert response.status_code == 200

    fetched = response.json()
    fetched_users = fetched["users"]
    total = fetched["total"]

    assert total == 5
    assert fetched_users[0]["id"] == users[5]["id"]
    assert fetched_users[4]["id"] == users[9]["id"]

    # test invalid page and limit
    response = await client.get("/users/?page=0&limit=5")
    assert response.status_code == 400

    response = await client.get("/users/?page=1&limit=0")
    assert response.status_code == 400
