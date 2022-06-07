from src.config import AppSettings
import logging


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Simple app to save user Notes online"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"