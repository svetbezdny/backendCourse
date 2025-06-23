async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": "2025-07-15", "date_to": "2025-08-20"},
    )
    assert response.status_code == 201
    res = response.json()
    assert isinstance(res, dict)
    assert res["transaction"] == "Successful"
    assert "data" in res
