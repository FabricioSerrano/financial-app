from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./financial_app/.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    DATABASE_URL: str
