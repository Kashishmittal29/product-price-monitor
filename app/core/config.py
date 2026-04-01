from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Price Monitor API"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./price_monitor.db"
    API_KEY: str = "secret-token-123"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
