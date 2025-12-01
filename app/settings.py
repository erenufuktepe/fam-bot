from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    BOT_TOKEN: str
    ALLOWED_USER_IDS: list[int]
    TZ: str = "America/Chicago"
    DATABASE_URL: str
    WEBHOOK_URL: str
    WEBHOOK_SECRET: str
    DEBUG: bool = False

    @property
    def tzinfo(self):
        return ZoneInfo(self.TZ)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = ","


settings = Settings()
