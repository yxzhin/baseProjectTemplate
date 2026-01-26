async def test_add_and_get_user_by_id(client, create_user):
    user = await create_user(737373373737, "ril73_test37")

    response = await client.get(f"/users/{user['discord_id']}")
    assert response.status_code == 200

    fetched = response.json()
    assert fetched["id"] == user["id"]
    assert fetched["discord_id"] == user["discord_id"]
    assert fetched["username"] == user["username"]
    assert fetched["avatar_url"] == user["avatar_url"]


async def test_add_and_get_user_by_username(client, create_user):
    user = await create_user(373737737373, "ril37_test73")

    response = await client.get(f"/users?username={user['username']}")
    assert response.status_code == 200

    fetched = response.json()
    assert fetched["id"] == user["id"]
    assert fetched["discord_id"] == user["discord_id"]
    assert fetched["username"] == user["username"]
    assert fetched["avatar_url"] == user["avatar_url"]
