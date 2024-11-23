from pydantic.v1 import BaseSettings
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    API_KEY: str
    OPEN_WEATHER_API_URL: str
    LOCAL_REDIS_HOST: str

    class Config:
        env_file = ROOT_DIR / ".env"
