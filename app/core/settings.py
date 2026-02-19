from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI with scalar"
    VERSION: str = "0.0.1"

settings = Settings()
