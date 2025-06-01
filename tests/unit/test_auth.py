from src.services.auth import AuthService


def test_create_access_token():
    access_token = AuthService().create_jwt_token(data={"username": "test"})
    assert access_token
    assert isinstance(access_token, str)
