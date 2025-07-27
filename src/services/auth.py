from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from src.config import settings
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_jwt_token(self, data: dict) -> str:
        data_copy = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        data_copy.update({"exp": expire})
        return jwt.encode(
            data_copy, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def decode_jwt_token(self, token: str) -> dict:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
