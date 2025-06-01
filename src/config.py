from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["local", "test", "dev", "prod"]

    DB_NAME: str
    DB_HOST: str
    DB_LOGIN: str
    DB_PASS: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_EXPIRE_SEC: int = 60

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_LOGIN}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
