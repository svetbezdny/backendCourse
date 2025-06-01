from src.services.auth import AuthService


def test_decode_and_encode_access_token():
    access_token = AuthService().create_jwt_token(data={"username": "test"})
    payload = AuthService().decode_jwt_token(access_token)
    assert payload
    assert payload["username"] == "test"
