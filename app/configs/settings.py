import os
from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and configuration."""

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Groq API
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama3-70b-8192"
    GROQ_STT_MODEL: str = "whisper-large-v3"

    # Audio Settings
    SAMPLE_RATE: int = 16000
    RECORDING_DURATION: float = 6.0  # seconds

    # Voice Settings
    VOICE_MODE: bool = True
    PUSH_TO_TALK: bool = True
    TTS_RATE: int = 175  # Words per minute

    # App Settings
    DEFAULT_TIMEZONE: str = "UTC"
    APPOINTMENT_SLOT_DURATION: int = 60  # minutes
    WORKING_HOURS: dict = {
        "start": 9,  # 9 AM
        "end": 17,  # 5 PM
    }

    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    LOGS_DIR: Path = BASE_DIR / "logs"

    def __init__(self, **data):
        super().__init__(**data)
        # Create necessary directories
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)


# Create settings instance
settings = Settings()
