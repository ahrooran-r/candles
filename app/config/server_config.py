from pydantic_settings import BaseSettings, SettingsConfigDict

from app.util.PathUtils import SERVER_ENV_FILE


class Settings(BaseSettings):
    # LEARN: Better to add defaults. Otherwise Python would say Parameter 'port' unfilled
    # I don't want to add default port. Let it fail fast if config is missing.
    port: int = None
    password: str = None

    model_config = SettingsConfigDict(env_file=SERVER_ENV_FILE)


settings: Settings = Settings()
