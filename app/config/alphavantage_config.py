from pydantic_settings import BaseSettings, SettingsConfigDict

from app.util.PathUtils import ALPHAVANTAGE_ENV_FILE


class Settings(BaseSettings):
    domain: str = None
    api_key: str = None
    request_rate: int = None
    demo_symbols: set[str] = None
    historical_depth: int = None

    model_config = SettingsConfigDict(env_file=ALPHAVANTAGE_ENV_FILE)


settings: Settings = Settings()
