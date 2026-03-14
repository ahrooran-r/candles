from pydantic_settings import BaseSettings, SettingsConfigDict

from app.util.PathUtils import ALPHAVANTAGE_ENV_FILE


class Settings(BaseSettings):
    domain: str = None
    api_key: str = None
    demo_symbols: set[str] = None

    model_config = SettingsConfigDict(env_file=ALPHAVANTAGE_ENV_FILE)


settings: Settings = Settings()
