from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FriendlyEats FastAPI"
    ENVIRONMENT: str = "local"
    FIREBASE_PROJECT_ID: str = "demo-friendlyeats"
    FIREBASE_CREDENTIALS_PATH: str | None = None
    FIRESTORE_EMULATOR_HOST: str | None = "127.0.0.1:8080"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
