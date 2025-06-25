async def test_authentication(ac):
    test_data = {
        "first_name": "John",
        "last_name": "Doe",
        "age": "30",
        "city": "New York",
        "email": "john_doe@test.com",
        "password": "test1234",
    }
    # register
    register_response = await ac.post("/auth/register", json=test_data)
    assert register_response.status_code == 201
    # login
    login_response = await ac.post("/auth/login", json=test_data)
    assert login_response.status_code == 200
    assert "access_token" in login_response.cookies
    # me
    me_response = await ac.get("/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["email"] == test_data["email"]
    # logout
    logout_response = await ac.post("/auth/logout")
    assert logout_response.status_code == 204
    assert logout_response.cookies.get("access_token") is None
    # me again
    me_response_again = await ac.get("/auth/me")
    assert me_response_again.status_code == 401
    assert "email" not in me_response_again.json()
