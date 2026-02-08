from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  app_name: str = "FastAPI Application"
  version: str = "1.0.0"
  database_url: str = "sqlite:///database.db"

settings = Settings()