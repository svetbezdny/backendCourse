from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
