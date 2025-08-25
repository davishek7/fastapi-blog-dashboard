import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseSettings(BaseSettings):
    MONGODB_URI: str = os.environ.get("MONGODB_URI")
    DB_NAME: str = os.environ.get("DB_NAME")


class EmailSettings(BaseSettings):
    MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM: str = os.environ.get("MAIL_FROM")
    MAIL_PORT: int = os.environ.get("MAIL_PORT")
    MAIL_SERVER: str = os.environ.get("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.environ.get("MAIL_FROM_NAME")
    MAIL_STARTTLS: bool = os.environ.get("MAIL_STARTTLS")
    MAIL_SSL_TLS: bool = os.environ.get("MAIL_SSL_TLS")
    USE_CREDENTIALS: bool = os.environ.get("USE_CREDENTIALS")
    VALIDATE_CERTS: bool = os.environ.get("VALIDATE_CERTS")


class GeneralSettings(BaseSettings):
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    TIMEZONE: str = "Asia/Kolkata"
    ACCESS_TOKEN_EXPIRE_TIMEDELTA: str = os.environ.get("ACCESS_TOKEN_EXPIRE_TIMEDELTA")
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: str = os.environ.get(
        "REFRESH_TOKEN_EXPIRE_TIMEDELTA"
    )
    VERIFICATION_TOKEN_EXPIRE_TIMEDELTA: str = os.environ.get(
        "VERIFICATION_TOKEN_EXPIRE_TIMEDELTA"
    )
    RESUME_URL: str = os.environ.get("RESUME_URL")
    BLOG_APP_URL: str = os.environ.get("BLOG_APP_URL")
    RESUME_APP_URL: str = os.environ.get("RESUME_APP_URL")
    DASHBOARD_APP_URL: str = os.environ.get("DASHBOARD_APP_URL")
    ALLOW_REGISTRATION: str = os.environ.get("ALLOW_REGISTRATION")


class Settings(DataBaseSettings, GeneralSettings, EmailSettings):
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
