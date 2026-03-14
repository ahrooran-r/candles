from pydantic_settings import BaseSettings, SettingsConfigDict

from app.util.PathUtils import DB_ENV_FILE


class Settings(BaseSettings):
    file_location: str = None

    model_config = SettingsConfigDict(env_file=DB_ENV_FILE)


settings: Settings = Settings()
