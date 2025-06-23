async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2023-07-15",
            "date_to": "2025-08-20",
        },
    )
    assert response.status_code == 200
