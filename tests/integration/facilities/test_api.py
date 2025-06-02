async def test_add_facilities(ac):
    response = await ac.post("/facilities/", json={"id": 1, "title": "test facilities"})
    assert response.status_code == 201


async def test_get_facilities(ac):
    response = await ac.get("/facilities/")
    assert response.status_code == 200
