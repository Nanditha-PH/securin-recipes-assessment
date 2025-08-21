from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL", default="postgresql+psycopg2://postgres:postgres@db:5432/recipes")
    port: int = Field(alias="PORT", default=8000)

    class Config:
        env_file = ".env"

settings = Settings()
