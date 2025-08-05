import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseSettings(BaseSettings):
    MONGODB_URI: str = os.environ.get("MONGODB_URI")
    DB_NAME: str = os.environ.get("DB_NAME")


class GeneralSettings(BaseSettings):
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    TIMEZONE: str = "Asia/Kolkata"


class Settings(DataBaseSettings, GeneralSettings):
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()