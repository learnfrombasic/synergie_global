from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    APP_NAME: str = "SyGlo"
    ROOT_DIR: Path = Path(".").resolve()
    GROQ_API_KEY: str
    GROQ_MODEL_NAME: str = "llama3.2-70b-instruct"
    GROQ_STT_MODEL: str = "whisper-large-v3"
    SAMPLE_RATE: int = 16000
    VOICE_MODE: bool = True
    PUSH_TO_TALK: bool = True


settings = Settings()

