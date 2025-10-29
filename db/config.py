from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10

    class Config:
        env_file = ".env"

settings = Settings()