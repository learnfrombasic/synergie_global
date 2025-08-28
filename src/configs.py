from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    GROQ_API_KEY: str
    GROQ_MODEL_NAME: str = "llama3.2-70b-instruct"
